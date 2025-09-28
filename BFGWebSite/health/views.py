# yourproject/health/views.py
from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache

def health(request):
    data = {"db": False, "cache": False}
    try:
        connections['default'].cursor()
        data['db'] = True
    except Exception:
        data['db'] = False

    try:
        cache.set('health-check', 'pong', 10)
        data['cache'] = cache.get('health-check') == 'pong'
    except Exception:
        data['cache'] = False

    status = 200 if all(data.values()) else 500
    return JsonResponse({"status": status, "checks": data}, status=status)
