from django import template
from django.utils.html import mark_safe
import json

register = template.Library()

@register.simple_tag
def product_jsonld(product):
    data = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": product.name,
        "image": [product.image.url] if product.image else [],
        "description": product.meta_description or product.description or '',
        "offers": {
            "@type": "Offer",
            "priceCurrency": "IRR",
            "price": str(product.current_price) if product.current_price is not None else "",
            "availability": "https://schema.org/InStock"
        }
    }
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')
