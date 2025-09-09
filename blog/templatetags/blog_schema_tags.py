from django import template
from django.utils.html import mark_safe
import json

register = template.Library()

@register.simple_tag
def article_jsonld(post):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post.title,
        "datePublished": post.published_at.isoformat() if post.published_at else '',
        "author": {"@type": "Person", "name": post.author},
        "description": post.meta_description or post.summary or ''
    }
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')
