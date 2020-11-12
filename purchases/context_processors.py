from .shoppinglist import ShoppingList


def shoplist(request):
    return {'shoplist': [recipe.slug for recipe in ShoppingList(request)]}
    