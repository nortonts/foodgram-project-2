from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from unidecode import unidecode


User = get_user_model()


class Tag:
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    TAGS = [BREAKFAST, LUNCH, DINNER]


class Ingredient(models.Model):
    title = models.CharField("Название", max_length=50)
    dimension = models.CharField("Единицы измерения", max_length=50)

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    name = models.CharField("Название", max_length=50, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    breakfast = models.BooleanField("Завтрак")
    lunch = models.BooleanField("Обед")
    dinner = models.BooleanField("Ужин")
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name="Ингридиенты", through="IngredientValue"
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления", help_text="в минутах"
    )
    description = models.TextField("Описание")
    image = models.ImageField("Фото", upload_to="recipes/")
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "recipe_detail",
            kwargs={"username": self.author.username, "slug": self.slug},
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def clean(self):
        if not self.breakfast and not self.lunch and not self.dinner:
            raise ValidationError("Необходимо выбрать хотя бы один тег.")

    def display_favorites(self):
        return ", ".join(
            self.favorites.all().values_list("user__username", flat=True)
        )

    display_favorites.short_description = "В избранном"


class IngredientValue(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name="ingredient_values",
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="ingredient_values",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    value = models.PositiveSmallIntegerField("Количество")

    class Meta:
        verbose_name = "Количество ингридиентов"
        verbose_name_plural = "Количество ингридиентов"

    def __str__(self):
        return str(self.value)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на {self.author}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.recipe} в избранном у {self.user}"
