from .shoppinglist import ShoppingList


def shoplist_size(request):
    return {'shoplist_size': len(ShoppingList(request))}