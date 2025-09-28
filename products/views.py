from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, PriceAlert
from django.views.generic.edit import FormView
from .forms import PriceAlertForm
from django.urls import reverse_lazy
from products.utils.analytics import send_ga_event  # مسیر به products.utils.analytics
from products.tasks import send_alert_confirmation_email  # اگر از Celery استفاده می‌کنی
from django.views import View
from .forms import CalculatorForm
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from news.models import News  # برای جستجوی اخبار هم
from django.views.decorators.http import require_GET



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = category.products.filter(is_active=True)
    return render(request, 'products/category_detail.html', {'category': category, 'products': products})

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    return render(request, 'products/product_detail.html', {'product': product})

# products/views.py (یا جایی که فرم را پردازش می‌کنی)

class PriceAlertCreateView(FormView):
    form_class = PriceAlertForm
    template_name = 'products/alert_form.html'
    success_url = reverse_lazy('products:alert_thanks')

    def get_initial(self):
        initial = super().get_initial()
        product_slug = self.request.GET.get('product') or self.request.POST.get('product_slug')
        if product_slug:
            initial['product_slug'] = product_slug
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product_slug = self.request.GET.get('product') or self.request.POST.get('product_slug')
        if product_slug:
            ctx['selected_product'] = Product.objects.filter(slug=product_slug).first()
        else:
            ctx['products_list'] = Product.objects.all().order_by('name')
        return ctx

    def form_valid(self, form):
        product = get_object_or_404(Product, slug=form.cleaned_data['product_slug'])
        alert = PriceAlert.objects.create(
            product=product,
            contact=form.cleaned_data['contact'],
            contact_method=form.cleaned_data['contact_method'],
            target_price=form.cleaned_data['target_price'],
            active=True,
            notified=False
        )

        client_id = self.request.POST.get('ga_client_id') or None
        send_ga_event('alert_create', {
            'product_id': product.slug,
            'product_name': product.name,
            'target_price': float(alert.target_price),
            'method': alert.contact_method,
        }, client_id=client_id)

        try:
            send_alert_confirmation_email.delay(alert.id)
        except Exception:
            from products.tasks import send_alert_confirmation_email_sync
            send_alert_confirmation_email_sync(alert.id)

        return super().form_valid(form)

def is_weight_unit(unit: str) -> bool:
    if not unit:
        return False
    u = unit.lower()
    return any(k in u for k in ['kg', 'کیلو', 'کیلوگرم', 'تن', 'ton'])

class CalculatorView(View):
    template_name = 'products/calculator.html'

    def get(self, request):
        product_slug = request.GET.get('product')
        form = CalculatorForm()
        products = Product.objects.all().order_by('name')
        selected = None
        if product_slug:
            selected = Product.objects.filter(slug=product_slug).first()
            if selected:
                form.initial['product_slug'] = selected.slug
                # قیمت server-side را فقط برای نمایش اولیه می‌گذاریم؛ محاسبه در سرور حتما از DB خوانده می‌شود
                form.initial['price'] = selected.current_price

        form.fields['product'].choices = [('', '— انتخاب کنید —')] + [(p.slug, p.name) for p in products]
        context = {'form': form, 'products': products, 'selected_product': selected, 'result': {}}
        return render(request, self.template_name, context)

    def post(self, request):
        products = Product.objects.all().order_by('name')
        form = CalculatorForm(request.POST)
        form.fields['product'].choices = [('', '— انتخاب کنید —')] + [(p.slug, p.name) for p in products]
        selected = None
        result = {}

        if form.is_valid():
            product_slug = form.cleaned_data.get('product_slug') or form.cleaned_data.get('product')
            if product_slug:
                selected = Product.objects.filter(slug=product_slug).first()

            # **همواره** قیمت و واحد را از DB می‌گیریم اگر محصول انتخاب شده باشد
            if selected:
                price = Decimal(selected.current_price or 0)
                unit = (selected.unit or '').strip()
            else:
                price = Decimal(form.cleaned_data.get('price') or 0)
                unit = ''

            quantity = form.cleaned_data.get('quantity')
            budget = form.cleaned_data.get('budget')

            if quantity:
                total = (Decimal(quantity) * price)
                if selected and is_weight_unit(unit):
                    display_qty = Decimal(quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    display_total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                else:
                    display_qty = int(Decimal(quantity).to_integral_value(rounding=ROUND_FLOOR))
                    display_total = (Decimal(display_qty) * price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                result = {
                    'mode': 'qty_to_price',
                    'quantity': display_qty,
                    'total': display_total,
                    'unit': unit,
                    'price': price
                }

            elif budget:
                if price == 0:
                    result = {'error': 'قیمت محصول صفر است؛ محاسبه ممکن نیست.'}
                else:
                    raw_qty = Decimal(budget) / price
                    if selected and is_weight_unit(unit):
                        display_qty = raw_qty.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    else:
                        display_qty = int(raw_qty.to_integral_value(rounding=ROUND_FLOOR))
                    result = {
                        'mode': 'budget_to_qty',
                        'quantity': display_qty,
                        'budget': Decimal(budget),
                        'unit': unit,
                        'price': price
                    }

        context = {'form': form, 'products': products, 'selected_product': selected, 'result': result}
        return render(request, self.template_name, context)
    
  # adjust import

def search_view(request):
    q = request.GET.get('q','').strip()
    results = {'products': [], 'news': []}
    if q:
        # ساده و موثر: icontains fallback اگر full-text نیست
        prods = Product.objects.filter(
            Q(name__icontains=q) | Q(meta_description__icontains=q)
        ).distinct()[:50]
        results['products'] = prods
        news_qs = News.objects.filter(is_published=True).filter(
            Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q)
        )[:20]
        results['news'] = news_qs
    return render(request, 'search/results.html', {'query': q, 'results': results})

def api_search(request):
    q = request.GET.get('q','').strip()
    out = {'products': [], 'news': []}
    if q and len(q) >= 2:
        prods = Product.objects.filter(Q(name__icontains=q) | Q(meta_description__icontains=q)).distinct()[:8]
        out['products'] = [{'name':p.name, 'url': p.get_absolute_url(), 'excerpt': (p.meta_description[:120] if getattr(p,'short_description',None) else '')} for p in prods]
        news_qs = News.objects.filter(is_published=True).filter(Q(title__icontains=q) | Q(summary__icontains=q))[:4]
        out['news'] = [{'title':n.title, 'url': n.get_absolute_url()} for n in news_qs]
    return JsonResponse(out)


@require_GET
def product_search_api(request):
    """
    AJAX search endpoint for Tom Select / Select2.
    Query: ?q=...
    Returns list of objects [{value, text, price, unit, id}, ...]
    """
    q = request.GET.get('q', '').strip()
    qs = Product.objects.all()
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(slug__icontains=q) |
            Q(category__name__icontains=q)  # optional
        )
    qs = qs.order_by('name')[:30]

    results = []
    for p in qs:
        results.append({
            "id": p.pk,
            "value": p.slug,                     # value used in <select>
            "text": f"{p.name} — {p.slug}",     # label shown in dropdown
            "price": int(p.current_price or 0),  # numeric price
            "unit": p.unit or ""
        })
    return JsonResponse(results, safe=False)

@require_GET
def product_detail_api(request, pk):
    """
    Return detailed info for a single product (used to populate price & unit).
    """
    try:
        p = Product.objects.get(pk=pk, is_active=True)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)
    return JsonResponse({
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'price': str(p.current_price if p.current_price is not None else ''),
        'unit': p.unit or ''
    })
