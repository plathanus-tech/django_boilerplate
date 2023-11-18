import pytest
from django.test.client import Client
from django.urls import reverse

from app.consts.http import HttpStatusCode
from users.models import User
from users.services import auth

AUTHENTICATION_URL_NAMES = ["api:v1:auth:auth-token", "api:v1:auth:auth-jwt-token"]


@pytest.mark.django_db
@pytest.mark.parametrize("url_name", AUTHENTICATION_URL_NAMES)
def test_auth_inexistent_account(client: Client, url_name):
    url = reverse(url_name)
    response = client.post(url, data={"username": "foo", "password": "foo"})
    assert response.status_code == HttpStatusCode.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["kind"] == auth.InactiveOrInexistentAccount.__name__
    assert "username" in data["extra"]["fields"]


@pytest.mark.django_db
@pytest.mark.parametrize("url_name", AUTHENTICATION_URL_NAMES)
def test_auth_inactive_account(client: Client, visitor_user: User, url_name):
    visitor_user.is_active = False
    visitor_user.save()

    url = reverse(url_name)
    response = client.post(
        url, data={"username": visitor_user.get_username(), "password": "password"}
    )
    assert response.status_code == HttpStatusCode.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["kind"] == auth.InactiveOrInexistentAccount.__name__
    assert "username" in data["extra"]["fields"]


@pytest.mark.django_db
@pytest.mark.parametrize("url_name", AUTHENTICATION_URL_NAMES)
def test_auth_succesfull_login(client: Client, visitor_user: User, url_name):
    url = reverse(url_name)
    response = client.post(
        url, data={"username": visitor_user.get_username(), "password": "password"}
    )
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    data = response.json()
    token_data = data["token"]
    assert "access" in token_data
    assert "refresh" in token_data
    assert "type" in token_data


@pytest.mark.django_db
def test_auth_jwt_refresh_token(client: Client, visitor_user: User):
    jwt_url = reverse("api:v1:auth:auth-jwt-token")
    token_response = client.post(
        jwt_url, data={"username": visitor_user.get_username(), "password": "password"}
    )
    assert token_response.status_code == HttpStatusCode.HTTP_200_OK
    refresh_token = token_response.json()["token"]["refresh"]
    assert refresh_token is not None, "Missing refresh token, check settings"

    refresh_url = reverse("api:v1:auth:auth-jwt-refresh")
    response = client.post(refresh_url, data={"refresh": refresh_token})
    assert response.status_code == HttpStatusCode.HTTP_200_OK
    refresh_data = response.json()
    assert "access" in refresh_data
    assert "refresh" in refresh_data
