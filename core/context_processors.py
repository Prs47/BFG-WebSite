# core/context_processors.py
from .models import SiteSetting
from django.conf import settings

def site_settings(request):
    """
    Context processor that returns first SiteSetting instance.
    Makes site_settings available in all templates as a variable.
    """
    return {'site_settings': SiteSetting.objects.first()}

def ga_settings(request):
    return {
        "GA_MEASUREMENT_ID": settings.GA_MEASUREMENT_ID,
    }
