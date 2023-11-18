import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from app.consts.http import HttpStatusCode
from users.models import User


def test_current_user_returns_unauthorized_on_non_logged_in(client: Client):
    url = reverse("api:v1:users:me-list")
    response = client.get(url)
    assert response.status_code == HttpStatusCode.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_current_user_returns_expected_output(visitor_user: User, client: Client):
    url = reverse("api:v1:users:me-list")
    client.force_login(visitor_user)
    response = client.get(url)
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    assert response.json() == {
        "id": visitor_user.id,
        "email": visitor_user.email,
        "full_name": visitor_user.full_name,
        "notification_token": visitor_user.notification_token,
        "language_code": {
            "value": visitor_user.language_code,
            "human": visitor_user.get_language_code_display(),
        },
        "time_zone": {
            "value": visitor_user.time_zone,
            "human": visitor_user.get_time_zone_display(),
        },
        "date_joined": timezone.localtime(visitor_user.date_joined).isoformat(),
        "is_staff": visitor_user.is_staff,
        "is_superuser": visitor_user.is_superuser,
    }


@pytest.mark.django_db
def test_current_user_delete_account_returns_unauthorized_on_non_logged_in(client: Client):
    url = reverse("api:v1:users:me-delete-account")
    response = client.delete(url)
    assert response.status_code == HttpStatusCode.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_current_user_delete_account_returns_expected_output(visitor_user: User, client: Client):
    url = reverse("api:v1:users:me-delete-account")
    client.force_login(visitor_user)
    response = client.delete(url)
    assert response.status_code == HttpStatusCode.HTTP_204_NO_CONTENT
    with pytest.raises(TypeError):
        # Since we don't return anything, trying to return JSON should fail
        response.json()
