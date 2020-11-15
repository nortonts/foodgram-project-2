from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.generics import get_object_or_404

from recipes.models import Ingredient, Subscription, Favorite, Recipe
from purchases.shoppinglist import ShoppingList


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["title", "dimension"]


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Subscription
        fields = ["id"]

    def validate(self, attrs):
        author_id = attrs.get("id")
        author = get_object_or_404(User, id=author_id)
        user = self.context.get("request").user

        if user == author:
            raise ValidationError(
                {"detail": "You can't subscribe to yourself"}
            )
        if Subscription.objects.filter(user=user, author=author).exists():
            raise ValidationError(
                {"detail": "You have already subscribed to this author"}
            )

        attrs["user"] = user
        attrs["author"] = author
        return attrs


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ["id"]

    def validate(self, attrs):
        recipe_id = attrs.get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.context.get("request").user

        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                {"detail": "This recipe is already in your favorites"}
            )

        attrs["user"] = user
        attrs["recipe"] = recipe
        return attrs


class ShoppingListSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def create(self, validated_data):
        recipe_id = validated_data.get("id")
        request = validated_data.get("request")
        shoppinglist = ShoppingList(request)
        shoppinglist.add(recipe_id)
        return shoppinglist
