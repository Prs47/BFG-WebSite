from django.contrib import admin
from .models import Category, Product, PriceHistory
from django.utils.html import format_html
from .models import PriceAlert


class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 1
    readonly_fields = ('date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'current_price', 'is_active', 'image_tag')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    inlines = [PriceHistoryInline]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'تصویر'

@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'contact', 'target_price', 'active', 'notified', 'created_at')
    list_filter = ('active', 'notified')
    search_fields = ('contact', 'product__name', 'product__slug')
