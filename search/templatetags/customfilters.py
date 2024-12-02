from django import template
from recipes.models import Recipe  # Adjust this import based on your app structure

register = template.Library()

@register.filter
def isinstance(value, class_str):
    return isinstance(value, Recipe)