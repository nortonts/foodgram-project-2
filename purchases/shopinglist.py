from recipes.models import Recipe


SHOPING_LIST_SESSION_ID = "shoping_list"


class ShopingList:

    def __init__(self, request):
        self.session = request.session
        shoping_list = self.session.get(SHOPING_LIST_SESSION_ID)
        if not shoping_list:
            shoping_list = self.session[SHOPING_LIST_SESSION_ID] = []
        self.shoping_list = shoping_list

    def add(self, recipe_id):
        if recipe_id not in self.shoping_list:
            self.shoping_list.append(recipe_id)
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, recipe_id):
        if recipe_id in self.shoping_list:
            self.shoping_list.remove(recipe_id)
            self.save()

    def __iter__(self):
        recipes_id = self.shoping_list
        recipes = Recipe.objects.filter(id__in=recipes_id)
        for recipe in recipes:
            yield recipe

    def __len__(self):
        return len(self.shoping_list)

    def clear(self):
        del self.session[SHOPING_LIST_SESSION_ID]
        self.save()
