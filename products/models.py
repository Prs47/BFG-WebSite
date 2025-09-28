# products/models.py
from django.db import models
from django.urls import reverse

UNIT_CHOICES = [
    ('kg', 'کیلوگرم'),
    ('branch', 'شاخه'),
]

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True, default='')
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    current_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    image_alt = models.CharField(max_length=250, blank=True, help_text="ALT متن برای سئو")
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # اگر Alt خالیست از نام محصول استفاده کن
        if not self.image_alt:
            self.image_alt = self.name
        super().save(*args, **kwargs)

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'تاریخچه قیمت'
        verbose_name_plural = 'تاریخچه قیمت‌ها'

    def __str__(self):
        return f"{self.product.name} - {self.price} - {self.date}"
    
class PriceAlert(models.Model):
    CONTACT_METHODS = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('telegram', 'Telegram'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    contact = models.CharField(max_length=200, help_text="email or phone number or telegram id")
    contact_method = models.CharField(max_length=20, choices=CONTACT_METHODS, default='email')
    target_price = models.DecimalField(max_digits=12, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.slug} -> {self.contact} <= {self.target_price}"
