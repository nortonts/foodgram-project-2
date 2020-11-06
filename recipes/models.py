from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from unidecode import unidecode

User = get_user_model()


# TAGS = (("Завтрак", "Завтрак"), ("Обед", "Обед"), ("Ужин", "Ужин"))


# class Tags(models.Model):
#     name = models.CharField("Название", max_length=50, choices=TAGS)
#     slug = models.SlugField()


class Ingredients(models.Model):
    name = models.CharField("Название", max_length=50)
    units = models.CharField("Единицы измерения", max_length=50)

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name


class Recepie(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author_recepie",
        verbose_name="Автор",
    )
    name = models.CharField("Название", max_length=50)
    slug = models.SlugField()
    breakfast = models.BooleanField("Завтрак")
    lunch = models.BooleanField("Обед")
    dinner = models.BooleanField("Ужин")
    ingredients = models.ManyToManyField(
        Ingredients, verbose_name="Ингридиенты", through="IngredientValue"
    )
    сooking_time = models.PositiveSmallIntegerField("Время приготовления")
    description = models.TextField("Описание")
    image = models.ImageField("Фото", upload_to="recepies/")
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
        return reverse("recepies_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def clean(self):
        if not self.breakfast and not self.lunch and not self.dinner:
            raise ValidationError("Необходимо выбрать хотя бы один тег.")


class IngredientValue(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        related_name="ingredient_value",
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
    )
    recepie = models.ForeignKey(
        Recepie,
        related_name="recepie_value",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    value = models.PositiveSmallIntegerField("Количество")

    class Meta:
        verbose_name = "Количество ингридиентов"
        verbose_name_plural = "Количество ингридиентов"
