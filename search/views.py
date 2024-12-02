from django.db.models import Q
from django.shortcuts import render
from itertools import chain
from recipes.models import Recipe
from blog.models import Blog_Post

# Create your views here.

def search_view(request):
    query = request.GET.get('q')
    if query:
        recipe_results = Recipe.objects.filter(
            Q(title__icontains=query) | Q(ingredients__icontains=query) | Q(method__icontains=query)
        )
        blog_results = Blog_Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        combined_results = list(chain(recipe_results, blog_results))
    else:
        combined_results = []
    
    return render(request, 'search/search_results.html', {'results': combined_results, 'query': query})