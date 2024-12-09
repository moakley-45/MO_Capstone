from django import template
from django.utils.html import strip_tags as django_strip_tags
from recipes.models import Recipe


register = template.Library()

@register.filter(name='is_recipe')
def is_recipe(value):
    return isinstance(value, Recipe)

@register.filter(name='strip_tags')
def strip_tags(value):
    return django_strip_tags(value)