from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            "name",
            "breakfast",
            "lunch",
            "dinner",
            "cooking_time",
            "description",
            "image",
        ]
