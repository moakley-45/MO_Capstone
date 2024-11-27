from . import views
from django.urls import path
from .views import BlogMainView

urlpatterns = [
    path('blog_main', BlogMainView.as_view(), name='blog main'),
    path('blog_post/<slug:slug>/', views.post_detail, name='blog post')
]

