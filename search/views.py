from django.db.models import Q
from itertools import chain
from django.shortcuts import render
from recipes.models import Recipe
from blog.models import Blog_Post


def search_view(request):
    query = request.GET.get('q')
    combined_results = []

    if query:
        recipe_results = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(method__icontains=query)
        )[:40]

        blog_results = Blog_Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )[:50]

        combined_results = list(chain(recipe_results, blog_results))

    return render(
        request,
        'search/search_results.html',
        {'results': combined_results, 'query': query}
    )
