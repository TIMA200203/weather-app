import pytest

from django.utils import timezone

from subscription.models import Subscription
from users.models import User


@pytest.fixture
def test_user_with_subscription(db):
    user = User.objects.create_user(
        username="test_username",
        password="test_password",
        email="test@email.com",
    )
    last_notification_time = timezone.now() - timezone.timedelta(days=2)
    subscription = Subscription.objects.create(
        pk=1,
        user=user,
        city="London",
        notification_period=24,
        last_notification_time=last_notification_time,
    )

    yield user, subscription

    subscription.delete()
    user.delete()
