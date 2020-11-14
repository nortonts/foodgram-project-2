from recipes.models import Recipe
from recipes.utils import get_ingredients


SHOPPINGLIST_SESSION_ID = "shoppinglist"


class ShoppingList:
    def __init__(self, request):
        self.session = request.session
        shoppinglist = self.session.get(SHOPPINGLIST_SESSION_ID)
        if not shoppinglist:
            shoppinglist = self.session[SHOPPINGLIST_SESSION_ID] = []
        self.shoppinglist = shoppinglist

    def add(self, recipe_id):
        if int(recipe_id) not in self.shoppinglist:
            self.shoppinglist.append(int(recipe_id))
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, recipe_id):
        if int(recipe_id) in self.shoppinglist:
            self.shoppinglist.remove(int(recipe_id))
            self.save()

    def __len__(self):
        return len(self.shoppinglist)

    def __iter__(self):
        recipes_id = self.shoppinglist
        recipes = Recipe.objects.filter(id__in=recipes_id)
        for recipe in recipes:
            yield recipe

    def clear(self):
        del self.session[SHOPPINGLIST_SESSION_ID]
        self.save()

    def get_ingridients_for_pdf(self):
        recipes_id = self.shoppinglist
        recipes = Recipe.objects.filter(id__in=recipes_id)
        ingridients_for_pdf = {}
        for recipe in recipes:
            recipe_ingridients = get_ingredients(recipe)
            for ingridient in recipe_ingridients:
                title, value, dimention = ingridient
                if ingridients_for_pdf.get(title):
                    ingridients_for_pdf[title][0] += value.value
                    ingridients_for_pdf[title][2].append(recipe.name)
                else:
                    ingridients_for_pdf[title] = [
                        value.value,
                        dimention,
                        [recipe.name],
                    ]

        ingridients_for_pdf = [
            [title, value[0], value[1], value[2]]
            for title, value in ingridients_for_pdf.items()
        ]

        return ingridients_for_pdf
