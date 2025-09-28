"""
URL configuration for BFGWebSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import BlogSitemap
from products.sitemaps import ProductSitemap, CategorySitemap
from django.conf import settings
from django.conf.urls.static import static
from BFGWebSite.health.views import health

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('products/', include('products.urls', namespace='products')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('contact/', include('contacts.urls', namespace='contacts')),
    path('news/', include('news.urls', namespace='news')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path("healthz/", health, name="healthz"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('core.urls')),
#     path('products/', include('products.urls', namespace='products')),
#     path('blog/', include('blog.urls', namespace='blog')),
#     path('contact/', include('contacts.urls', namespace='contacts')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)