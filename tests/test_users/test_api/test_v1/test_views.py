from django.test import Client
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


def testAuthReturnsAuthRefreshTokens(admin_user: User, client: Client):
    url = reverse("users:api:v1:auth")
    response = client.post(
        url,
        data={"email": admin_user.email, "password": "password"},
        content_type="application/json",
    )
    assert response.status_code == 200, "Unable to authenticate with correct credentials"
    data = response.json()
    expected_keys = ["user", "access", "refresh", "token_type"]

    for key in expected_keys:
        assert key in data, f"{key=} not present on response data"


def testAuthFailsForWrongCredentials(admin_user: User, client: Client):
    url = reverse("users:api:v1:auth")
    response = client.post(
        url, data={"email": admin_user.email, "password": "Wrong"}, content_type="application/json"
    )
    assert response.status_code == 400, "Expected to return bad response"


def testRefreshReturnsNewAccessRefreshTokens(admin_user: User, client: Client):
    url = reverse("users:api:v1:refresh")
    response = client.post(
        url,
        data={"refresh": str(RefreshToken.for_user(admin_user))},
        content_type="application/json",
    )
    assert response.status_code == 200, "Expected to return a refresh token for the user"

    data = response.json()
    assert "refresh" in data
    assert "access" in data


def testDeleteInactivatesUser(admin_user: User, admin_client: Client):
    url = reverse("users:api:v1:delete")
    admin_client.delete(url)

    admin_user.refresh_from_db()
    assert not admin_user.is_active, "User was not inactivated"
