from django.urls import path
from .views import BlogMainView, blog_post_detail, comment_edit, comment_delete

urlpatterns = [
    path('', BlogMainView.as_view(), name='blog_main'),  
    path('<slug:slug>/', blog_post_detail, name='blog_post_detail'),
    path('<slug:slug>/edit/<int:comment_id>/', comment_edit, name='comment_edit'),
    path('<slug:slug>/delete/<int:comment_id>/', comment_delete, name='comment_delete'),
]