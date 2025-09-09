from django.contrib.syndication.views import Feed
from .models import BlogPost

class LatestPostsFeed(Feed):
    title = "BFGWebSite - تازه‌ها"
    link = "/blog/"
    description = "آخرین مقالات و اخبار بازار آهن"

    def items(self):
        return BlogPost.objects.filter(published=True).order_by('-published_at')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary or item.content[:200]
