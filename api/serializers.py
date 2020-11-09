from rest_framework import serializers

from recipes.models import Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredients
        fields = ["title", "dimension"]
