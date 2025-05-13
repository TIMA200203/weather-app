import json

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.test.client import Client

from subscription.models import Subscription
from users.models import User


@pytest.mark.django_db
def test_create_subscription_api(client: Client, test_user: User):
    client.login(username=test_user.email, password=test_user.password)

    post_data = {"user": 10, "city": "New-York", "notification_period": 12}
    response = client.post(reverse("subscription_api:create"), post_data)
    assert response.status_code == 201

    subscription = Subscription.objects.get(id=response.data["pk"])
    assert subscription.city == "New-York"


NEW_NOTIFICATION_PERIOD = 3


@pytest.mark.django_db
def test_edit_subscription_api(
    client: Client, test_user_with_subscription: tuple[User, Subscription]
):
    test_user, subscription = test_user_with_subscription
    client.login(username=test_user.email, password=test_user.password)

    put_data = {"notification_period": NEW_NOTIFICATION_PERIOD}
    response = client.put(
        reverse(
            "subscription_api:edit",
            kwargs={"subscription_id": subscription.id},
        ),
        data=json.dumps(put_data),
        content_type="application/json",
    )
    assert response.status_code == 200

    subscription = Subscription.objects.get(id=response.data["pk"])
    assert subscription.notification_period == NEW_NOTIFICATION_PERIOD


@pytest.mark.django_db
def test_delete_subscription_api(
    client: Client, test_user_with_subscription: tuple[User, Subscription]
):
    test_user, subscription = test_user_with_subscription
    client.login(username=test_user.email, password=test_user.password)

    deleted_id = subscription.id

    response = client.delete(
        reverse(
            "subscription_api:delete", kwargs={"subscription_id": deleted_id}
        )
    )
    assert response.status_code == 204

    with pytest.raises(ObjectDoesNotExist):
        Subscription.objects.get(id=deleted_id)


@pytest.mark.django_db
def test_subscription_list_api(
    client: Client, test_user_with_subscription: tuple[User, Subscription]
):
    test_user, _ = test_user_with_subscription
    client.login(username=test_user.email, password=test_user.password)

    response = client.get(
        reverse(
            "subscription_api:list", kwargs={"username": test_user.username}
        )
    )

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_disable_subscription_api(
    client: Client, test_user_with_subscription: tuple[User, Subscription]
):
    test_user, subscription = test_user_with_subscription
    client.login(username=test_user.email, password=test_user.password)

    response = client.post(
        reverse(
            "subscription_api:disable",
            kwargs={"subscription_id": subscription.id},
        )
    )
    assert response.status_code == 200

    subscription.refresh_from_db()
    assert not subscription.is_enabled


@pytest.mark.django_db
def test_enable_subscription_api(
    client: Client, test_user_with_subscription: tuple[User, Subscription]
):
    test_user, subscription = test_user_with_subscription
    client.login(username=test_user.email, password=test_user.password)
    subscription.is_enabled = False
    subscription.save()

    response = client.post(
        reverse(
            "subscription_api:enable",
            kwargs={"subscription_id": subscription.id},
        )
    )
    assert response.status_code == 200

    subscription.refresh_from_db()
    assert subscription.is_enabled
