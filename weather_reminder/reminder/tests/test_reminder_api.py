import pytest

from django.shortcuts import reverse
from django.test.client import Client
from django.utils import timezone

from subscription.models import Subscription
from users.models import User


@pytest.mark.django_db
def test_get_subscription_for_notification(
    client: Client, test_user_with_subscription: tuple[User, Subscription]
):
    response = client.get(reverse("weather_api:get_subscription"))
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_subscription(
    client: Client, test_user_with_subscription: tuple[User, Subscription]
):
    _, subscription = test_user_with_subscription

    subscription_id = 1
    post_data = {"subscription_ids": [subscription_id]}
    response = client.post(
        reverse("weather_api:update_last_notification_time"), post_data
    )
    assert response.status_code == 200

    updated_subscription = Subscription.objects.get(pk=subscription_id)

    assert (
        subscription.last_notification_time
        != updated_subscription.last_notification_time
    )
    max_allowed_difference = timezone.timedelta(minutes=1)
    time_difference = abs(
        updated_subscription.last_notification_time - timezone.now()
    )
    assert time_difference <= max_allowed_difference
