from django.urls import reverse
from django.test.client import Client


def test_admin_login(client: Client):
    url = reverse("admin:login")
    response = client.get(url)
    assert response.status_code == 200, url
