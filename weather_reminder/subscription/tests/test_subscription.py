import pytest
from django.shortcuts import reverse
from django.test.client import Client

from users.models import User


@pytest.mark.django_db
def test_subscription_list_view(client: Client, test_user: User):
    client.login(username=test_user.email, password=test_user.password)

    response = client.get(reverse("subscription:subscriptions"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_subscription_view(client: Client, test_user: User):
    client.login(username=test_user.email, password=test_user.password)

    response = client.post(reverse("subscription:create"))
    assert response.status_code == 302
