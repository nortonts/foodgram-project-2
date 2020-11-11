from django.urls import path

from . import views


urlpatterns = [
    path(
        "", views.shoppinglist_detail, name="shoppinglist_detail"
    ),
]
