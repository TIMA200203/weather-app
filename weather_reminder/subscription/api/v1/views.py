from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView

from subscription.api.v1.serializers import SubscriptionSerializer
from subscription.models import Subscription

from users.models import User


class SubscriptionAPI(APIView):

    def post(self, request: HttpRequest) -> Response:
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request: HttpRequest, subscription_id: int) -> Response:
        try:
            subscription = Subscription.objects.get(pk=subscription_id)
        except ObjectDoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

        serializer = SubscriptionSerializer(
            subscription, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request: HttpRequest, subscription_id: int) -> Response:
        try:
            subscription = Subscription.objects.get(pk=subscription_id)
        except ObjectDoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

        subscription.delete()
        return Response(status=204)


class SubscriptionList(APIView):

    def get(self, request: HttpRequest, username: str) -> Response:
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(
                {"error": f"User {username} not found"}, status=404
            )
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=200)


class DisableSubscription(APIView):
    def post(self, request: HttpRequest, subscription_id: int) -> Response:
        try:
            subscription = Subscription.objects.get(pk=subscription_id)
        except ObjectDoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

        if not subscription.is_enabled:
            return Response(
                {"message": "Subscription already disabled"}, status=200
            )

        subscription.is_enabled = False
        subscription.save()
        return Response({"message": "Subscription disabled"}, status=200)


class EnableSubscription(APIView):
    def post(self, request: HttpRequest, subscription_id: int) -> Response:
        try:
            subscription = Subscription.objects.get(pk=subscription_id)
        except ObjectDoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

        if subscription.is_enabled:
            return Response(
                {"message": "Subscription already enabled"}, status=200
            )

        subscription.is_enabled = True
        subscription.save()
        return Response({"message": "Subscription enabled"}, status=200)
