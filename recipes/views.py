from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Recipe, CUISINE_CHOICES
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class RecipeView(generic.ListView):
    model = Recipe
    template_name = "recipes/recipes_main.html"
    context_object_name = 'recipes_pages'
    paginate_by = 9 

    def get_queryset(self):
        return Recipe.objects.all().order_by('-created_on')

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