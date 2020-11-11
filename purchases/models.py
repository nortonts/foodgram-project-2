from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()


class ShopingList(models.Model):
    user = models.ForeignKey(
        User, related_name="shoping_list", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="shoping_list", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"

    def __str__(self):
        return f"Список покупок {self.user} по рецепту {self.recipe}"
