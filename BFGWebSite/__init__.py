# BFGWebSite/__init__.py
try:
    from .celery import app as celery_app
except Exception as e:
    # اگر celery نصب نبود یا خطایی رخ داد، لاگ کن و ادامه بده
    celery_app = None
    # برای دیباگ می‌تونی لاگ بنویسی، ولی در production نذار پر سر و صدا باشه:
    import logging
    logging.getLogger(__name__).warning("Celery not available at import time: %s", e)
