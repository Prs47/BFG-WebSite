import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BFGWebSite.settings')

app = Celery('BFGWebSite')
# namespace='CELERY' باعث می‌شود متغیرهای تنظیمی از settings با پیشوند CELERY_ خوانده شوند
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # اتوماتیک tasks را از اپ‌ها می‌یابد
