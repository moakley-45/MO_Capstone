from django import template
from recipes.models import Recipe

register = template.Library()

@register.filter(name='is_recipe')
def is_recipe(value):
    return isinstance(value, Recipe)