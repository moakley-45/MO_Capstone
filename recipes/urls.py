from django.urls import path
from . import views

app_name = 'recipes' 

urlpatterns = [
    path('', views.RecipeView.as_view(), name='recipes_main'),
    path('<slug:slug>/', views.recipes_page, name='recipes_page'),
    path('cuisine/<str:cuisine>/', views.cuisine_specific_recipes, name='cuisine_recipes'),
]
