from . import views
from django.urls import path
from .views import BlogMainView

urlpatterns = [
    path('', BlogMainView.as_view(), name='blog_main'),
    path('<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
]
