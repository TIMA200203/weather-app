import pytest

from subscription.models import Subscription
from users.models import User


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        pk=10,
        username="test_username",
        password="test_password",
        email="test@email.com",
    )

    yield user

    user.delete()


@pytest.fixture
def test_user_with_subscription(db):
    user = User.objects.create_user(
        username="test_username",
        password="test_password",
        email="test@email.com",
    )
    subscription = Subscription.objects.create(
        user=user, city="Kiev", notification_period=24
    )

    yield user, subscription

    subscription.delete()
    user.delete()
