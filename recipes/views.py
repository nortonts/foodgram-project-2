from django.views.generic import ListView, DetailView

from .models import Recipe


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