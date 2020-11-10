from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    get_object_or_404,
)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from recipes.models import Ingredients, Subscription
from .serializers import IngredientsSerializer, SubscriptionSerializer


User = get_user_model()


class IngredientsListAPIView(ListAPIView):
    serializer_class = IngredientsSerializer

    def get_queryset(self):
        queryset = Ingredients.objects.all()
        query = self.request.query_params.get("query", None)

        if query is not None:
            queryset = queryset.filter(title__icontains=query)

        return queryset


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        user = self.request.user
        author_id = self.request.data.get("id")
        author = get_object_or_404(User, id=author_id)
        if user == author:
            raise ValidationError(
                {"detail": "You can't subscribe to yourself"}
            )
        serializer.save(user=user, author=author)


class SubscriptionDeleteAPIView(DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        Subscription.objects.filter(
            user=self.request.user, author=self.get_object()
        ).delete()
        return Response(data={"success": True})
