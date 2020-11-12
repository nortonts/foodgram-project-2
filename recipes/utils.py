from django.shortcuts import get_object_or_404

from .models import Ingredients, IngredientValue


def get_ingredients(recipe):
    ingredients = []
    for ingredient in recipe.ingredients.all():
        value = ingredient.ingredient_value.get(recipe=recipe)
        ingredients.append((ingredient.title, value, ingredient.dimension))
    return ingredients


def create_ingridients(recipe, data):
    for key, value in data.items():
        arg = key.split("_")
        if arg[0] == "nameIngredient":
            title = value
        if arg[0] == "valueIngredient":
            ingredient = get_object_or_404(Ingredients, title=title)
            IngredientValue.objects.update_or_create(
                ingredient=ingredient, recipe=recipe, defaults={"value": value}
            )
