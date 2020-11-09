from django.urls import include, path

from . import views


urlpatterns = [
    path(
        "ingredients/",
        views.IngredientsListAPIView.as_view(),
        name="ingredients_list",
    ),
]