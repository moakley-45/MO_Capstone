from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Blog_Post

class BlogMainView(generic.ListView):
    model = Blog_Post
    template_name = "blog/blog_main.html"
    context_object_name = 'blog_posts'
    paginate_by = 5 

    def get_queryset(self):
        return Blog_Post.objects.all().order_by('-created_on')

def blog_post_detail(request, slug):
    """
    Display an individual :model:`blog.Blog_Post`.

    **Context**

    ``blog_post``
        An instance of :model:`blog.Blog_Post`.

    **Template:**

    :template:`blog/blog_post.html`
    """

    queryset = Blog_Post.objects.filter(status=1)
    blog_post = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "blog/blog_post.html",
        {"blog_post": blog_post},
    )