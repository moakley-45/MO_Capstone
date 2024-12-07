from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Recipe, CUISINE_CHOICES, Review, ReviewComment
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .forms import RecipeForm, ReviewForm, ReviewCommentForm
from django.urls import reverse
from django.views.generic import TemplateView
from django.utils.text import slugify
import random


class RecipeView(generic.ListView):
    model = Recipe
    template_name = "recipes/recipes_main.html"
    context_object_name = 'recipes_pages'
    paginate_by = 9 

    def get_queryset(self):
        sort_by = self.request.GET.get('sort', '-created_on')
        queryset = Recipe.objects.all()

        # Filter out AdminTeam recipes if requested
        user_submitted = self.request.GET.get('user_submitted', 'false').lower() == 'true'
        if user_submitted:
            queryset = queryset.exclude(creator__username='AdminTeam')

        if sort_by == 'alphabetical':
            return queryset.order_by('title')
        elif sort_by == 'oldest':
            return queryset.order_by('created_on')
        else:  # newest first (default)
            return queryset.order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', '-created_on')
        context['user_submitted'] = self.request.GET.get('user_submitted', 'false').lower() == 'true'
        return context

def recipes_page(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, status=1)
    reviews = recipe.reviews.all()
    review_form = ReviewForm()
    comment_form = ReviewCommentForm()
    
    context = {
        "recipe": recipe,
        "reviews": reviews,
        "review_form": review_form,
        "comment_form": comment_form,
    }
    return render(request, "recipes/recipes_page.html", context)


def cuisine_specific_recipes(request, cuisine):
    recipes = Recipe.objects.filter(cuisine=cuisine, status=1) 
    return render(request, 'recipes/cuisine_specific.html', {
        'recipes': recipes,
        'cuisine': dict(CUISINE_CHOICES)[cuisine]
    })

def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    reviews = recipe.reviews.all()
    review_form = ReviewForm()
    comment_form = ReviewCommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        if 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.author = request.user
                review.recipe = recipe
                review.save()
                messages.success(request, 'Your review has been successfully submitted!')
                return redirect('recipes:recipe_detail', slug=slug)
        elif 'comment_submit' in request.POST:
            comment_form = ReviewCommentForm(request.POST)
            if comment_form.is_valid():
                review_id = request.POST.get('review_id')
                review = get_object_or_404(Review, id=review_id)
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.review = review
                comment.approved = False
                comment.save()
                messages.success(request, 'Your comment has been successfully submitted and is awaiting approval.')
                return redirect('recipes:recipe_detail', slug=slug)

    context = {
        'recipe': recipe,
        'reviews': reviews,
        'review_form': review_form,
        'comment_form': comment_form,
    }
    return render(request, 'recipes/recipes_page.html', context)

@login_required
def edit_review(request, slug, review_id):
    recipe = get_object_or_404(Recipe, slug=slug)
    review = get_object_or_404(Review, id=review_id, author=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.approved = False
            review.save()
            messages.success(request, 'Your review has been updated and is awaiting re-approval from our Admin Team. Check back soon!')
            return redirect('recipes:recipe_detail', slug=slug)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'recipe': recipe,
        'review': review,
    }
    return render(request, 'recipes/edit_review.html', context)

@login_required
def delete_review(request, slug, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.author:
        messages.error(request, "You can only delete your own reviews.")
        return redirect('recipes:recipe_detail', slug=slug)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been successfully deleted.')
        return redirect('recipes:recipe_detail', slug=slug)
    
    return render(request, 'recipes/delete_review_confirm.html', {'review': review})

@login_required
def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            
            recipe.slug = slugify(recipe.title)  
            
            recipe.save()
            print(f"Recipe slug: {recipe.slug}") 
            
            messages.success(request, 'Your recipe has been submitted successfully! Our Admin Team will quickly review it and make it Live as soon as possible - please check back soon!')

            return redirect('home') 
    else:
        form = RecipeForm()
    return render(request, 'recipes/submit_recipe.html', {'form': form})

@login_required
def submit_review(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.recipe = recipe
            review.approved = False
            review.save()
            messages.success(request, 'Your review has been successfully submitted! It will be moderated by our Admin Team and made live ASAP - please check back soon!')
            return redirect('recipes:recipe_detail', slug=slug)
        else:
            messages.error(request, 'There was an error submitting your review. Please re-check your input details!')
    else:
        review_form = ReviewForm()

    reviews = recipe.reviews.filter(approved=True)
    context = {
        'recipe': recipe,
        'review_form': review_form,
        'reviews': reviews,
    }
    return render(request, 'recipes/recipes_page.html', context)

@login_required
def add_review_comment(request, slug, review_id):
    recipe = get_object_or_404(Recipe, slug=slug)
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            ReviewComment.objects.create(
                review=review,
                author=request.user,
                body=body,
                approved=False
            )
    return redirect('recipes:recipe_detail', slug=slug)

@login_required
def review_comment_edit(request, slug, review_id, comment_id):
    recipe = get_object_or_404(Recipe, slug=slug)
    review = get_object_or_404(Review, id=review_id)
    comment = get_object_or_404(ReviewComment, pk=comment_id)

    if request.method == "POST":
        comment_form = ReviewCommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.approved = False
            comment.save()
            messages.success(request, 'Comment Updated!')
        else:
            messages.error(request, 'Error updating comment!')

    return redirect('recipes:recipe_detail', slug=slug)

@login_required
def review_comment_delete(request, slug, review_id, comment_id):
    recipe = get_object_or_404(Recipe, slug=slug)
    review = get_object_or_404(Review, id=review_id)
    comment = get_object_or_404(ReviewComment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted!')
    else:
        messages.error(request, 'You can only delete your own comments!')

    return redirect('recipes:recipe_detail', slug=slug)