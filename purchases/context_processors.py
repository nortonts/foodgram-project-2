from .shoppinglist import ShoppingList


def shoplist(request):
    shoppinglist = ShoppingList(request)
    return {
        "shoplist": shoppinglist.get_objects().values_list("slug", flat=True)
    }
