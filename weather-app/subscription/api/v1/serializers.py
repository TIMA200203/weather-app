from rest_framework import serializers

from subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    is_enabled = serializers.BooleanField(default=True)

    class Meta:
        model = Subscription
        fields = ("pk", "user", "city", "notification_period", "is_enabled")
