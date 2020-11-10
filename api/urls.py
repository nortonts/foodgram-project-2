from django.urls import include, path

from . import views


urlpatterns = [
    path(
        "subscriptions/<int:pk>/",
        views.SubscriptionDeleteAPIView.as_view(),
        name="delete_subscriptions",
    ),    
    path(
        "subscriptions/",
        views.SubscriptionCreateAPIView.as_view(),
        name="create_subscriptions",
    ),
    path(
        "favorites/<int:pk>/",
        views.FavoriteDeleteAPIView.as_view(),
        name="delete_favorites",
    ), 
    path(
        "favorites/",
        views.FavoriteCreateAPIView.as_view(),
        name="create_favorites",
    ),
    path(
        "ingredients/",
        views.IngredientsListAPIView.as_view(),
        name="ingredients_list",
    ),
]