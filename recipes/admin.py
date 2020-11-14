from django.contrib import admin

from .models import (
    Ingredient,
    IngredientValue,
    Recipe,
    Subscription,
    Favorite,
)


class IngredientValueInline(admin.StackedInline):
    model = IngredientValue


@admin.register(Recipe)
class RecepieAdmin(admin.ModelAdmin):
    inlines = [
        IngredientValueInline,
    ]
    prepopulated_fields = {"slug": ("name",)}

    list_display = ("name", "pub_date", "author", "display_favorites")

    fieldsets = (
        (None, {"fields": ("author", "name", "slug")}),
        (
            "Теги",
            {
                "fields": (
                    (
                        "breakfast",
                        "lunch",
                        "dinner",
                    ),
                )
            },
        ),
        (
            "Информация и фото",
            {
                "fields": (
                    "cooking_time",
                    "description",
                    "image",
                ),
            },
        ),
    )

    list_filter = ("author", "name", "breakfast", "lunch", "dinner")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension")
    search_fields = ("title",)


admin.site.register(Subscription)
admin.site.register(Favorite)
