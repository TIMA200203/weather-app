from django.db.models import DurationField, ExpressionWrapper, F, IntegerField
from django.db.models.functions import ExtractDay, ExtractHour, ExtractMinute
from django.http import HttpRequest
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView

from reminder.api.v1.serializers import UserSubscriptionSerializer

from subscription.models import Subscription


class NotificationSubscription(APIView):
    def get(self, request: HttpRequest) -> Response:
        notification_time = timezone.now()

        time_difference_expression = ExpressionWrapper(
            notification_time - F("last_notification_time"),
            output_field=DurationField(),
        )
        subscriptions_with_time_dif = Subscription.objects.annotate(
            time_difference_hours=ExpressionWrapper(
                ExtractDay(time_difference_expression) * 24
                + ExtractHour(time_difference_expression)
                + ExtractMinute(time_difference_expression) / 60,
                output_field=IntegerField(),
            )
        )
        subscriptions = subscriptions_with_time_dif.filter(
            is_enabled=True,
            time_difference_hours__gte=F("notification_period"),
        ).select_related("user")
        serializer = UserSubscriptionSerializer(subscriptions, many=True)

        return Response(serializer.data)


class UpdateLastNotificationTime(APIView):
    def post(self, request: HttpRequest) -> Response:
        subscription_ids = request.data.get("subscription_ids", [])
        subscriptions = Subscription.objects.filter(id__in=subscription_ids)
        now = timezone.now()

        updated_subscriptions = []
        for subscription in subscriptions:
            subscription.last_notification_time = now
            updated_subscriptions.append(subscription)

        Subscription.objects.bulk_update(
            updated_subscriptions, ["last_notification_time"]
        )

        return Response(status=200)
