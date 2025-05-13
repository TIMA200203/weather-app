from django.shortcuts import reverse
from django.test.client import Client


def test_main(client: Client):
    response = client.get(reverse("main:index"))
    assert response.status_code == 200
