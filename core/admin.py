# from django.contrib import admin
# from .models import SiteSetting

# @admin.register(SiteSetting)
# class SiteSettingAdmin(admin.ModelAdmin):
#     list_display = ('site_name', 'phone', 'address')

from django.contrib import admin
from .models import SiteSetting
from django.utils.html import format_html
from django import forms

class SiteSettingAdminForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = '__all__'
        widgets = {
            'google_map_embed': forms.Textarea(attrs={'rows':4, 'cols':40}),
            'opening_hours': forms.Textarea(attrs={'rows':3}),
        }

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    form = SiteSettingAdminForm
    list_display = ('site_name','phone','address')
