# products/utils.py
import csv
from io import StringIO
from decimal import Decimal, InvalidOperation
from django.db import transaction
from products.models import Product, PriceHistory
import logging

logger = logging.getLogger(__name__)

def import_prices_from_csv_content(csv_text, source='csv'):
    """
    خواندن متن CSV، بروز‌رسانی product.current_price فقط وقتی قیمت واقعا تغییر کند،
    و اضافه کردن یک PriceHistory جدید در آن صورت.
    خروجی: {'updated': n, 'skipped': m}
    """
    updated = 0
    skipped = 0
    reader = csv.DictReader(StringIO(csv_text))
    with transaction.atomic():
        for row in reader:
            slug = (row.get('slug') or '').strip()
            price_raw = (row.get('price') or '').strip()
            if not slug or not price_raw:
                logger.warning("Skipping row with missing slug/price: %s", row)
                skipped += 1
                continue
            try:
                price_val = Decimal(price_raw.replace(',', '').strip())
            except (InvalidOperation, ValueError) as e:
                logger.warning("Skipping row with invalid price %r: %s", price_raw, e)
                skipped += 1
                continue

            p = Product.objects.filter(slug=slug).first()
            if not p:
                logger.warning("Skipping unknown product slug=%s", slug)
                skipped += 1
                continue

            old_price = p.current_price
            # only create history if price changed (or old_price is None)
            try:
                if old_price is None or Decimal(str(old_price)) != price_val:
                    PriceHistory.objects.create(product=p, price=price_val, source=source)
                    p.current_price = price_val
                    p.save(update_fields=['current_price'])
                    updated += 1
                else:
                    skipped += 1
            except Exception as e:
                logger.exception("Error updating price for %s: %s", slug, e)
                skipped += 1

    return {'updated': updated, 'skipped': skipped}
