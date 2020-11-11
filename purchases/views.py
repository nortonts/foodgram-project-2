from django.shortcuts import render

from .shoppinglist import ShoppingList


def shoppinglist_detail(request):
    shopping_list = ShoppingList(request)
    return render(
        request,
        "purchases/shopList.html",
        {"shopping_list": shopping_list, "current_page": "shopping_list"},
    )
