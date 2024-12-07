from django.urls import path
from . import views

app_name = 'recipes' 

urlpatterns = [
    path('', views.RecipeView.as_view(), name='recipes_main'),
    path('submit-recipe/', views.submit_recipe, name='submit_recipe'),
    path('cuisine/<str:cuisine>/', views.cuisine_specific_recipes, name='cuisine_recipes'),
    path('<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('<slug:slug>/review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<slug:slug>/review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('<slug:slug>/submit-review/', views.submit_review, name='submit_review'),
    path('<slug:slug>/review/<int:review_id>/comment/', views.add_review_comment, name='add_review_comment'),
    path('<slug:slug>/review/<int:review_id>/comment/<int:comment_id>/edit/', views.review_comment_edit, name='review_comment_edit'),
    path('<slug:slug>/review/<int:review_id>/comment/<int:comment_id>/delete/', views.review_comment_delete, name='review_comment_delete'),
]



