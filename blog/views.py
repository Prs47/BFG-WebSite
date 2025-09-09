from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.contrib.syndication.views import Feed

def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('-published_at')
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_detail(request, post_slug):
    post = get_object_or_404(BlogPost, slug=post_slug, published=True)
    return render(request, 'blog/blog_detail.html', {'post': post})

class LatestPostsFeed(Feed):
    title = "BFGWebSite - تازه‌ها"
    link = "/blog/"
    description = "آخرین مقالات"

    def items(self):
        return BlogPost.objects.filter(published=True).order_by('-published_at')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary or item.content[:200]
