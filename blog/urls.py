from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<slug:post_slug>/', views.blog_detail, name='post_detail'),
    path('feed/', views.LatestPostsFeed(), name='blog_feed'),  # feed view later
]
