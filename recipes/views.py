from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Recipe, CUISINE_CHOICES, Review, ReviewComment
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .forms import RecipeForm, ReviewCommentForm
from django.urls import reverse
from django.views.generic import TemplateView
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
    queryset = Recipe.objects.filter(status=1)
    recipe = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "recipes/recipes_page.html",
        {
        "recipe": recipe,
        },
    )

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
                return redirect('recipe_detail', slug=slug)
        elif 'comment_submit' in request.POST:
            comment_form = ReviewCommentForm(request.POST)
            if comment_form.is_valid():
                review_id = request.POST.get('review_id')
                review = get_object_or_404(Review, id=review_id)
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.review = review
                comment.save()
                messages.success(request, 'Your comment has been successfully submitted and is awaiting approval.')
                return redirect('recipe_detail', slug=slug)

    context = {
        'recipe': recipe,
        'reviews': reviews,
        'review_form': review_form,
        'comment_form': comment_form,
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def edit_review(request, slug, review_id):
    recipe = get_object_or_404(Recipe, slug=slug)
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.author:
        messages.error(request, "You can only edit your own reviews.")
        return redirect('recipe_detail', slug=slug)
    
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect('recipe_detail', slug=slug)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'recipes/edit_review.html', {'form': form, 'recipe': recipe})

@login_required
def delete_review(request, slug, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.author:
        messages.error(request, "You can only delete your own reviews.")
    else:
        review.delete()
        messages.success(request, "Your review has been deleted.")
    return redirect('recipe_detail', slug=slug)  

def your_view(request):
    context = {
        'CUISINE_CHOICES': CUISINE_CHOICES,
        # ... other context variables ...
    }
    return render(request, 'cuisine_specific.html', context)


@login_required
def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.creator = request.user
            recipe.save()
            return redirect(reverse('recipes:recipe_detail', kwargs={'slug': recipe.slug}))
    else:
        form = RecipeForm()
    return render(request, 'recipes/submit_recipe.html', {'form': form})


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_recipes = list(Recipe.objects.all())
        random_recipes = random.sample(all_recipes, min(2, len(all_recipes)))
        context['random_recipes'] = random_recipes
        return context