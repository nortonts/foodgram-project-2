from django.urls import path

from . import views


urlpatterns = [
    path("create/", views.RecipeCreateView.as_view(), name="recipe_create"),
    path(
        "<str:username>/",
        views.AuthorRecipeListView.as_view(),
        name="author_recipe_list",
    ),
    path(
        "<str:username>/subscription/",
        views.SubscriptionListView.as_view(),
        name="subscription_list",
    ),
    path(
        "<str:username>/favorite/",
        views.FavoriteRecipeListView.as_view(),
        name="favorite_list",
    ),
    path(
        "<str:username>/<str:slug>/edit/",
        views.RecipeUpdateView.as_view(),
        name="recipe_edit",
    ),
    path(
        "<str:username>/<str:slug>/delete/",
        views.RecipeDeleteView.as_view(),
        name="recipe_delete",
    ),
    path(
        "<str:username>/<str:slug>/",
        views.RecipeDetailView.as_view(),
        name="recipe_detail",
    ),
    path("", views.RecipeListView.as_view(), name="recipe_list"),
]
