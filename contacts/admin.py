from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at', 'seen')
    list_filter = ('seen',)
    search_fields = ('name', 'phone')
