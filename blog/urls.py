from . import views
from django.urls import path
from .views import BlogMainView

urlpatterns = [
    path('', BlogMainView.as_view(), name='blog_main'),
    path('<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>', views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>', views.comment_delete, name='comment_delete'),
]
