from rest_framework.generics import ListAPIView

from recipes.models import Ingredients
from .serializers import IngredientsSerializer


class IngredientsListAPIView(ListAPIView):
    serializer_class = IngredientsSerializer

    def get_queryset(self):
        queryset = Ingredients.objects.all()
        query = self.request.query_params.get('query', None)
        
        if query is not None:
            queryset = queryset.filter(title__icontains=query)
            
        return queryset
