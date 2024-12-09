from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from .models import Blog_Post, Comment
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib import messages

class BlogMainView(generic.ListView):
    model = Blog_Post
    template_name = "blog/blog_main.html"
    context_object_name = 'blog_posts'
    paginate_by = 6 

    def get_queryset(self):
        return Blog_Post.objects.all().order_by('-created_on')

def blog_post_detail(request, slug):
    queryset = Blog_Post.objects.filter(status=1)
    blog_post = get_object_or_404(queryset, slug=slug)
    comments = blog_post.comments.all().order_by("-created_on")
    comment_count = blog_post.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = blog_post 
            comment.save()
            messages.success(request, 'Your comment has been successfully submitted and is awaiting approval from our Admin team - check back soon!')
            return redirect('blog:blog_post_detail', slug=slug)  
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
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
    return redirect('blog:blog_post_detail', slug=slug)  

@login_required
def comment_edit(request, slug, comment_id):
    """
    View to edit comments.
    """
    queryset = Blog_Post.objects.filter(status=1)
    blog_post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment_form.save() 
            messages.success(request, 'Comment Updated!')
            return redirect('blog:blog_post_detail', slug=slug)
        else:
            messages.error(request, 'Error updating comment!')

    else:
        comment_form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {
        'form': comment_form,
        'blog_post': blog_post,
        'comment': comment,
    })

@login_required
def comment_delete(request, slug, comment_id):
    """
    View to delete a comment.
    """
    queryset = Blog_Post.objects.filter(status=1)
    blog_post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted!')
    else:
        messages.error(request, 'You can only delete your own comments!')

    return redirect('blog:blog_post_detail', slug=slug)  