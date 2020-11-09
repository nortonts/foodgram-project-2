from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import RecipeForm
from .models import Ingredients, IngredientValue, Recipe


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

            ingredient_name = form.cleaned_data["ingredient_name"]
            ingredient_value = form.cleaned_data["ingredient_value"]
            ingredient = get_object_or_404(Ingredients, name=ingredient_name)

            IngredientValue.objects.create(
                ingredient=ingredient, recipe=recipe, value=ingredient_value
            )
            form.save_m2m()
            return redirect("recipe_detail", recipe.slug)

        return render(request, "recipes/recipe_form.html", {"form": form})


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "recipe"
        return context

    def get(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.user != recipe.author:
            return redirect("recipe_detail", recipe.slug)
        return super().get(request, *args, **kwargs)
