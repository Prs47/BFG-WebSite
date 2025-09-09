# # core/models.py

# from django.db import models

# class SiteSetting(models.Model):
#     site_name = models.CharField(max_length=200, default="BFGWebSite")
#     phone = models.CharField(max_length=50, blank=True)
#     address = models.CharField(max_length=255, blank=True)
#     google_map_embed = models.TextField(blank=True, help_text="iframe embed code for Google Map")
#     latitude = models.CharField(max_length=50, blank=True)
#     longitude = models.CharField(max_length=50, blank=True)
#     opening_hours = models.CharField(max_length=255, blank=True)
#     meta_default_description = models.CharField(max_length=300, blank=True)

#     class Meta:
#         verbose_name = "تنظیمات سایت"
#         verbose_name_plural = "تنظیمات سایت"

#     def __str__(self):
#         return self.site_name

from django.db import models
from django.contrib.postgres.fields import JSONField  # اگر از Postgres استفاده می‌کنی
# اگر نسخه جنگو < 3.1 و بدون JSONField در db، می‌توان از TextField استفاده کرد

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, default="BFGWebSite", help_text="نام نمایش‌داده‌شده سایت")
    phone = models.CharField(max_length=50, blank=True, help_text="شماره تلفن رسمی")
    address = models.CharField(max_length=255, blank=True, help_text="آدرس کامل (برای نمایش در تماس/فوتر)")
    google_map_embed = models.TextField(blank=True, help_text="کد iframe از Google Maps (Share → Embed a map)")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, help_text="مختصات عرض جغرافیایی")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, help_text="مختصات طول جغرافیایی")
    opening_hours = models.JSONField(blank=True, null=True, help_text='مثال: {"Mo-Fr": "08:00-17:00", "Sa": "09:00-13:00"}')
    meta_default_description = models.CharField(max_length=300, blank=True, help_text="توضیحات دیفالت برای متا")

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return self.site_name
