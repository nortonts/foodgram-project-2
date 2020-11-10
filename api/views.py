from django.contrib.auth import get_user_model

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    get_object_or_404,
)

from .serializers import IngredientsSerializer, SubscriptionSerializer
from recipes.models import Ingredients, Subscription

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
        author_id = self.request.POST.get("id")
        author = get_object_or_404(User, id=author_id)
        serializer.save(user=user, author=author)


class SubscriptionDeleteAPIView(DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    # def perform_destroy(self, author):
    #     Subscription.objects.filter(
    #         user=self.request.user, 
    #         author=author
    #     ).delete()
    

# @login_required
# def profile_follow(request, username):
#     follower = request.user
#     following = get_object_or_404(User, username=username)
#     if follower != following:
#         Follow.objects.get_or_create(user=follower, author = following)
#     return redirect(profile, username)


# @login_required
# def profile_unfollow(request, username):
#     follower = request.user
#     following = get_object_or_404(User, username=username)
#     Follow.objects.filter(user=follower, author = following).delete()
#     return redirect(profile, username)
