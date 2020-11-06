from django.urls import path

from . import views


urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path("<slug>/", views.RecipeDetailView.as_view(), name ="recipe_detail")
]
