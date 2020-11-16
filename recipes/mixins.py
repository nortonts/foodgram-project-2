from django.db.models import Q
from django.shortcuts import redirect

from .models import Recipe, Tag


class RecipeMixin:
    model = Recipe
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "recipe"
        filters = self.request.GET.getlist(
            "filters", Tag.TAGS
        )
        context["filters"] = "&" + "&".join([f"filters={f}" for f in filters])
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query_filters = self.request.GET.getlist("filters", Tag.TAGS)

        if len(query_filters) == 1:
            f = dict.fromkeys(query_filters, True)
            return queryset.filter(**f)

        if len(query_filters) == 2:
            f1 = dict.fromkeys([query_filters[0]], True)
            f2 = dict.fromkeys([query_filters[1]], True)
            return queryset.filter(Q(**f1) | Q(**f2))

        return queryset


class IsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return redirect(
                "recipe_detail", kwargs.get("username"), kwargs.get("slug")
            )
        return super().dispatch(request, *args, **kwargs)
