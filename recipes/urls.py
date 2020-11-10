from django.urls import path

from . import views


urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path(
        "author/<str:username>",
        views.AuthorRecipeListView.as_view(),
        name="author_recipe_list",
    ),
    path("create/", views.RecipeCreateView.as_view(), name="recipe_create"),
    path(
        "<str:slug>/edit/",
        views.RecipeUpdateView.as_view(),
        name="recipe_edit",
    ),
    path(
        "<str:slug>/", views.RecipeDetailView.as_view(), name="recipe_detail"
    ),
]
