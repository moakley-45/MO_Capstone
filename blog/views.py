from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Blog_Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib import messages

class BlogMainView(generic.ListView):
    model = Blog_Post
    template_name = "blog/blog_main.html"
    context_object_name = 'blog_posts'
    paginate_by = 5 

    def get_queryset(self):
        return Blog_Post.objects.all().order_by('-created_on')

def blog_post_detail(request, slug):
    queryset = Blog_Post.objects.filter(status=1)
    blog_post = get_object_or_404(queryset, slug=slug)
    comments = blog_post.comments.all().order_by("-created_on")
    comment_count = blog_post.comments.filter(approved=True).count()

    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = blog_post 
            comment.save()
            messages.success(request, 'Your comment has been successfully submitted and is awaiting approval from our Admin team - check back soon!')
            return redirect('blog_post_detail', slug=slug)
    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/blog_post.html",
        {
        "blog_post": blog_post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        },
    )

@login_required
def add_comment(request, blog_post_id):
    blog_post = get_object_or_404(Blog_Post, id=blog_post_id)
    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Comment.objects.create(
                post=blog_post,
                author=request.user,
                body=body,
                approved=False
            )
    return redirect('blog_post_detail', slug=blog_post.slug)