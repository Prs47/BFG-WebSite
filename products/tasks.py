# products/tasks.py
import os
import logging
import requests
from celery import shared_task
from django.conf import settings
from .utils import import_prices_from_csv_content
from .notifications import send_price_alerts_for_product  # see below or simple impl

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def fetch_and_import_prices(self):
    url = getattr(settings, 'PRICES_CSV_URL', None) or os.environ.get('PRICES_CSV_URL')
    logger.info("fetch_and_import_prices: PRICES_CSV_URL=%s", url)
    if not url:
        return {'error': 'no csv url configured'}
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        text = resp.text
        result = import_prices_from_csv_content(text, source='remote')
        # after import, optionally trigger check alerts (sync or async)
        from .tasks import check_price_alerts
        check_price_alerts.delay()
        return result
    except Exception as e:
        logger.exception("fetch_and_import_prices failed: %s", e)
        return {'error': str(e)}

@shared_task(bind=True)
def check_price_alerts(self):
    """
    بررسی همه‌ی PriceAlertهای فعال؛ اگر شرط برقرار باشه، ارسال نوتیف و set notified=True
    """
    from .models import PriceAlert
    notified = 0
    checked = 0
    alerts = PriceAlert.objects.filter(active=True, notified=False).select_related('product')
    for a in alerts:
        checked += 1
        try:
            current = a.product.current_price
            if current is None:
                continue
            # logic: notify if current <= target_price
            if current <= a.target_price:
                # send notification (email/telegram)
                from .notifications import send_price_alert_email, send_telegram_alert
                if a.contact_method == 'email':
                    send_price_alert_email(a.contact, a.product, a.target_price)
                elif a.contact_method == 'telegram':
                    send_telegram_alert(a.contact, a.product, a.target_price)
                # mark as notified
                a.notified = True
                a.active = False
                a.save(update_fields=['notified','active'])
                notified += 1
        except Exception as e:
            logger.exception("Error checking alert id=%s: %s", a.id, e)
    return {'checked': checked, 'notified': notified}
