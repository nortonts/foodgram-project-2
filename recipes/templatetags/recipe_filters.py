from django import template

from recipes.models import Favorite


register = template.Library()


@register.filter
def is_favorite(recipe_id, user_id):
    return Favorite.objects.filter(
        user_id=user_id, recipe_id=recipe_id
    ).exists()


@register.filter
def plural_recipe(number):
    if number % 10 == 1 and number not in (11, 111):
        ending = ""
    elif 1 < number % 10 < 5 and number not in (12, 13, 14, 112, 113, 114):
        ending = "а"
    else:
        ending = "ов"
    return ending
