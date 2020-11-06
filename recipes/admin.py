from django.contrib import admin

from .models import Ingredients, IngredientValue, Recepie

class IngredientValueInline(admin.StackedInline):
    model = IngredientValue


@admin.register(Recepie)
class RecepieAdmin(admin.ModelAdmin):
    inlines = [IngredientValueInline,]
    prepopulated_fields = {"slug": ("name",)}
    
    list_display = ("name", "pub_date", "author")

    fieldsets = (
        (None, {'fields': ('author', 'name', 'slug')}),
        ("Теги", {'fields': (("breakfast", "lunch", "dinner",),)}),
        ("Информация и фото", {
            'fields': ("сooking_time", "description", "image",),
        }),
    )

    list_filter = (
        "author",
        "name",
        "breakfast", 
        "lunch", 
        "dinner"
    )

    # TODO На странице рецепта вывести число добавлений этого рецепта в избранное.


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ("name", "units")
    # TODO Добавить фильтр по названию.
