from django.urls import path
from . import views

app_name = 'recipes' 

urlpatterns = [
    path('', views.RecipeView.as_view(), name='recipes_main'),
    path('submit-recipe/', views.submit_recipe, name='submit_recipe'),
    path('cuisine/<str:cuisine>/', views.cuisine_specific_recipes, name='cuisine_recipes'),
    path('<slug:slug>/', views.recipes_page, name='recipes_page'),
    path('<slug:slug>/review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<slug:slug>/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]