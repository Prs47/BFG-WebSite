from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from products.models import Product, PriceHistory

class Command(BaseCommand):
    help = 'Import prices from CSV (columns: slug,price,source)'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        path = options['csv_path']
        updated = 0
        skipped = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            with transaction.atomic():
                for row in reader:
                    slug = row.get('slug')
                    price = row.get('price')
                    source = row.get('source', 'csv')
                    if not slug or not price:
                        self.stdout.write(self.style.WARNING(f"Missing slug or price in row: {row}"))
                        skipped += 1
                        continue
                    try:
                        p = Product.objects.get(slug=slug)
                        PriceHistory.objects.create(product=p, price=price, source=source)
                        p.current_price = price
                        p.save(update_fields=['current_price'])
                        updated += 1
                    except Product.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Product {slug} not found"))
                        skipped += 1
        self.stdout.write(self.style.SUCCESS(f"Import finished. Updated: {updated}, Skipped: {skipped}"))
