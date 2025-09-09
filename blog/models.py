# blog/models.py
from django.db import models
from django.urls import reverse

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField()
    summary = models.CharField(max_length=500, blank=True)
    author = models.CharField(max_length=150, default='BFGWebSite')
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    tags = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
