from recipes.models import Recipe


SHOPPING_LIST_SESSION_ID = "shoping_list"


class ShoppingList:

    def __init__(self, request):
        self.session = request.session
        shopping_list = self.session.get(SHOPPING_LIST_SESSION_ID)
        if not shopping_list:
            shopping_list = self.session[SHOPPING_LIST_SESSION_ID] = []
        self.shopping_list = shopping_list

    def add(self, recipe_id):
        if int(recipe_id) not in self.shopping_list:
            self.shopping_list.append(int(recipe_id))
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, recipe_id):
        if int(recipe_id) in self.shopping_list:
            self.shopping_list.remove(int(recipe_id))
            self.save()

    def __len__(self):
        return len(self.shopping_list)

    def __iter__(self):
        recipes_id = self.shopping_list
        recipes = Recipe.objects.filter(id__in=recipes_id)
        for recipe in recipes:
            yield recipe

    def clear(self):
        del self.session[SHOPPING_LIST_SESSION_ID]
        self.save()
