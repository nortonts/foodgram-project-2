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
        query_filters = self.request.GET.getlist(
            "filters", Tag.TAGS
        )
        filters = dict.fromkeys(Tag.TAGS, False)
        for f in query_filters:
            del filters[f]
        return queryset.filter(**filters)


class IsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return redirect(
                "recipe_detail", kwargs.get("username"), kwargs.get("slug")
            )
        return super().dispatch(request, *args, **kwargs)
