from django.shortcuts import render, get_object_or_404
from .models import News

# Create your views here.

def news_list(request):
    qs = News.objects.filter(is_published=True)
    return render(request, 'news/list.html', {'news_list': qs})

def news_detail(request, slug):
    obj = get_object_or_404(News, slug=slug, is_published=True)
    return render(request, 'news/detail.html', {'news': obj})

