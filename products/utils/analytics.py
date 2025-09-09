# utils/analytics.py
import os
import uuid
import requests
import logging

logger = logging.getLogger(__name__)

MEASUREMENT_ID = os.getenv("GA_MEASUREMENT_ID")
API_SECRET = os.getenv("GA_API_SECRET")

def send_ga_event(name: str, params: dict = None, client_id: str = None):
    """
    ارسال سرور-ساید به GA4 via Measurement Protocol.
    client_id: اگر از مرورگر فرستادی بفرست؛ در غیر اینصورت uuid ساخته می‌شود.
    """
    if not MEASUREMENT_ID or not API_SECRET:
        logger.debug("GA not configured (missing MEASUREMENT_ID/API_SECRET).")
        return False
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"
    payload = {
        "client_id": client_id or str(uuid.uuid4()),
        "events": [{"name": name, "params": params or {}}]
    }
    try:
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
        logger.info("GA event sent: %s", name)
        return True
    except Exception as e:
        logger.exception("Failed to send GA event %s: %s", name, e)
        return False
