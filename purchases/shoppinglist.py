from recipes.models import Recipe
from recipes.utils import get_ingredients


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

    def get_ingridients_for_pdf(self):
        recipes_id = self.shopping_list
        recipes = Recipe.objects.filter(id__in=recipes_id)
        ingridients_dict = {}
        for recipe in recipes:
            ingridients = get_ingredients(recipe)
            for ingridient in ingridients:
                title, value, dimention = ingridient
                if ingridients_dict.get(title):
                    ingridients_dict[title][0] += value.value
                    ingridients_dict[title][2].append(recipe.name)
                else:
                    ingridients_dict[title] = [
                        value.value,
                        dimention,
                        [recipe.name],
                    ]

        ingridients_list = [
            [title, value[0], value[1], value[2]]
            for title, value in ingridients_dict.items()
        ]

        return ingridients_list
