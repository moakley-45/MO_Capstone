from . import views
from django.urls import path
from .views import BlogMainView

urlpatterns = [
    path('blog_main', BlogMainView.as_view(), name='blog main'),
    path('/<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
]

