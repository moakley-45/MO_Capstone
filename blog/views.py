from django.shortcuts import render
from django.views import generic
from .models import Blog_Post

class BlogMainView(generic.ListView):
    model = Blog_Post
    template_name = "blog/blog_main.html"
    context_object_name = 'blog_posts'
    paginate_by = 5 

    def get_queryset(self):
        return Blog_Post.objects.all().order_by('-created_on') 