from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import PriceAlertCreateView
from .views import CalculatorView

app_name = 'products'

urlpatterns = [
    path('search/', views.search_view, name='search'),
    path('api/search/', views.api_search, name='api_search'),
    path('calculator/', CalculatorView.as_view(), name='calculator'),
    path('alerts/create/', PriceAlertCreateView.as_view(), name='alert_create'),
    path('', views.category_list, name='category_list'),
    path('item/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('alerts/thanks/', TemplateView.as_view(template_name='products/alert_thanks.html'), name='alert_thanks'),
    path('<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('api/product-search/', views.product_search_api, name='product_search_api'),
    path('api/<int:pk>/', views.product_detail_api, name='api_product_detail'),
]
