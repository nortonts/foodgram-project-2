from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .utils import get_ingredients, create_ingridients
from .mixins import RecipeMixin, IsAuthorMixin
from .forms import RecipeForm
from .models import (
    Recipe,
    Subscription,
    Favorite,
)


User = get_user_model()


class RecipeDetailView(DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context["current_page"] = "recipe"
        context["ingredients"] = get_ingredients(recipe)
        if self.request.user.is_authenticated:
            context["is_subscribed"] = Subscription.objects.filter(
                author=recipe.author, user=self.request.user
            ).exists()
            context["is_favorite"] = Favorite.objects.filter(
                user=self.request.user, recipe=recipe
            ).exists()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "create_recipe"
        return context

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()
        create_ingridients(recipe, self.request.POST)
        form.save_m2m()
        return redirect(
            "recipe_detail", recipe.author.username, recipe.slug
        )

    def form_invalid(self, form):
        return render(self.request, "recipes/recipe_form.html", {"form": form})


class RecipeUpdateView(LoginRequiredMixin, IsAuthorMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "recipe"
        context["ingredients"] = get_ingredients(self.get_object())
        return context

    def form_valid(self, form):
        self.object.ingredient_values.all().delete()
        create_ingridients(self.object, self.request.POST)
        form.save()
        return redirect(
            "recipe_detail", self.object.author.username, self.object.slug
        )

    def form_invalid(self, form):
        return render(self.request, "recipes/recipe_form.html", {"form": form})


class RecipeDeleteView(LoginRequiredMixin, IsAuthorMixin, DeleteView):
    model = Recipe

    def get_success_url(self):
        return reverse_lazy(
            "author_recipe_list", args=[self.request.user.username]
        )

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        return self.post(*args, **kwargs)


class RecipeListView(RecipeMixin, ListView):
    pass


class AuthorRecipeListView(RecipeMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs.get("username"))
        context["author"] = author
        if self.request.user.is_authenticated:
            context["is_subscribed"] = Subscription.objects.filter(
                author=author, user=self.request.user
            ).exists()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.kwargs.get("username")
        if username is not None:
            queryset = queryset.filter(author__username=username)
        return queryset


class FavoriteRecipeListView(LoginRequiredMixin, RecipeMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "favorite"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        recipe_ids = Favorite.objects.filter(
            user=self.request.user
        ).values_list("recipe_id", flat=True)
        return queryset.filter(id__in=recipe_ids)


class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "subscription"
        return context

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
