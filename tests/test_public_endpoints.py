import pytest
from django.test.client import Client
from django.urls import reverse


@pytest.mark.parametrize(
    "reversable,",
    [
        ("admin:login"),
        ("admin_password_reset"),
    ],
)
def test_admin_login(client: Client, reversable: str):
    url = reverse(reversable)
    response = client.get(url)
    assert response.status_code == 200, url
