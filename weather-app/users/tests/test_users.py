import pytest
from django.shortcuts import reverse
from django.test.client import Client

from users.models import User


@pytest.mark.django_db
def test_auth(client: Client):
    response = client.get(reverse("users:register"))
    assert response.status_code == 200
    register_post_data = {
        "username": "test_user",
        "email": "test_email@gmail.com",
        "password": "test_password",
        "confirm_password": "test_password",
    }
    response = client.post(reverse("auth_api:register"), register_post_data)
    assert response.status_code == 200

    test_user = User.objects.get(email="test_email@gmail.com")
    assert test_user.username == "test_user"

    response = client.get(reverse("users:login"))
    assert response.status_code == 200

    login_post_data = {
        "email": "test_email@gmail.com",
        "password": "test_password",
    }

    response = client.post(reverse("auth_api:login"), login_post_data)
    assert response.status_code == 200

    login_required_response = client.get(reverse("subscription:subscriptions"))
    assert login_required_response.status_code == 200

    response = client.post(reverse("auth_api:logout"))
    assert response.status_code == 200

    login_required_response = client.get(reverse("subscription:subscriptions"))
    assert login_required_response.status_code == 302
