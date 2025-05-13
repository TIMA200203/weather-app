from rest_framework import serializers

from subscription.models import Subscription


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user_pk = serializers.PrimaryKeyRelatedField(
        source="user.pk", read_only=True
    )
    user_email = serializers.EmailField(source="user.email")

    class Meta:
        model = Subscription
        fields = ("pk", "user_pk", "user_email", "city")
