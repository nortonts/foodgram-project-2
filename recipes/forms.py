from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    ingredient_name = forms.CharField(max_length=50)
    ingredient_value = forms.IntegerField(max_value=10000, min_value=0)

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

