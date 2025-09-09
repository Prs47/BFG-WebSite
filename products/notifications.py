# products/notifications.py
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
logger = logging.getLogger(__name__)

def send_price_alerts_for_product(alert):
    """
    wrapper simple: expects a PriceAlert instance `alert`
    and sends via email or telegram based on alert.contact_method.
    """
    try:
        if alert.contact_method == 'email':
            send_price_alert_email(alert.contact, alert.product, alert.target_price)
        elif alert.contact_method == 'telegram':
            send_telegram_alert(alert.contact, alert.product, alert.target_price)
        else:
            logger.warning("Unknown contact_method for alert id=%s: %s", getattr(alert,'id',None), alert.contact_method)
    except Exception as e:
        logger.exception("Failed to send alert id=%s: %s", getattr(alert,'id',None), e)

def send_price_alert_email(to_email, product, target_price):
    subject = f"هشدار قیمت برای {product.name}"
    context = {"product": product, "target_price": target_price}

    text_content = render_to_string("emails/price_alert.txt", context)
    html_content = render_to_string("emails/price_alert.html", context)

    msg = EmailMultiAlternatives(subject, text_content, None, [to_email])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        logger.info("✅ ایمیل هشدار برای %s ارسال شد.", to_email)
    except Exception as e:
        logger.exception("❌ خطا در ارسال ایمیل: %s", e)
        
def send_telegram_alert(chat_id, product, target_price):
    # برای تست ساده لاگ کن
    logger.info("Would send Telegram to %s about %s target=%s", chat_id, product.slug, target_price)
