from rest_framework import serializers
from rest_framework.serializers import ValidationError

from recipes.models import Ingredients, Subscription, Favorite
from purchases.shoppinglist import ShoppingList


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ["title", "dimension"]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ["id"]

    def save(self, **kwargs):
        user = kwargs.get("user")
        author = kwargs.get("author")
        if user == author:
            raise ValidationError(
                {"detail": "You can't subscribe to yourself"}
            )
        if Subscription.objects.filter(user=user, author=author).exists():
            raise ValidationError(
                {"detail": "You have already subscribed to this author"}
            )
        return super().save(**kwargs)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ["id"]

    def save(self, **kwargs):
        user = kwargs.get("user")
        recipe = kwargs.get("recipe")
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                {"detail": "This recipe is already in your favorites"}
            )
        return super().save(**kwargs)


class ShoppingListSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def create(self, validated_data):
        recipe_id = validated_data.get("id")
        request = validated_data.get("request")
        shoppinglist = ShoppingList(request)
        shoppinglist.add(recipe_id)
        return shoppinglist
