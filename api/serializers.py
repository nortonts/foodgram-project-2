from rest_framework import serializers

from recipes.models import Ingredients, Subscription, Favorite


class IngredientsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredients
        fields = ["title", "dimension"]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ["id"]

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ["id"]
