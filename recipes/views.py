from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Recipe, CUISINE_CHOICES
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .forms import RecipeForm
from django.urls import reverse


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