from .models import Recipe


class RecipeMixin:
    model = Recipe
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "recipe"
        filters = self.request.GET.getlist(
            "filters", ["breakfast", "lunch", "dinner"]
        )
        context["filters"] = "&" + "&".join([f"filters={f}" for f in filters])
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query_filters = self.request.GET.getlist(
            "filters", ["breakfast", "lunch", "dinner"]
        )
        filters = dict.fromkeys(["breakfast", "lunch", "dinner"], False)
        for f in query_filters:
            del filters[f]
        return queryset.filter(**filters)
