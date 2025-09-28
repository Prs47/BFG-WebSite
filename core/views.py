from django.shortcuts import render
from products.models import Product
from blog.models import BlogPost
from django.http import HttpResponse
from contacts.forms import ContactForm
from news.models import News
from django.conf import settings

def home_view(request):
    products = Product.objects.filter(is_active=True).order_by('-id')[:12]
    recent_news = News.objects.filter(is_published=True)[:3]
    site_hero_image = None
    # اگر site settings یا مدل تنظیمات داری می‌تونی image را از آنجا بگیری
    return render(request, 'core/home.html', {'products': products, 'recent_news': recent_news, 'site_hero_image': site_hero_image})


def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def about(request):
    # می‌توان اینجا site_settings و هر اطلاعات دیگری ارسال کرد (context processor این کار را می‌کند)
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # ContactMessage مدل از contacts.models
            return render(request, 'core/thankyou_contact.html')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
