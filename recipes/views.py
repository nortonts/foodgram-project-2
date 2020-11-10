from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import RecipeForm
from .models import Ingredients, IngredientValue, Recipe


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


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "recipe"
        return context


class RecipeDetailView(DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "recipe"
        context["ingredients"] = get_ingredients(self.get_object())
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "create_recipe"
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            create_ingridients(recipe, request.POST)
            form.save_m2m()
            return redirect("recipe_detail", recipe.slug)
        return render(request, "recipes/recipe_form.html", {"form": form})


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "recipe"
        context["ingredients"] = get_ingredients(self.get_object())
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            return redirect("recipe_detail", self.object.slug)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object.recepie_value.all().delete()
            create_ingridients(self.object, request.POST)
            form.save()
            return redirect("recipe_detail", self.object.slug)
        return render(request, "recipes/recipe_form.html", {"form": form})


class AuthorRecipeListView(ListView):
    model = Recipe
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "recipe"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.kwargs.get("username")
        if username:
            queryset = queryset.filter(author__username=username)
        return queryset
