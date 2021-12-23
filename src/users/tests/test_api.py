from django.test.client import Client as TestClient
from users.models import User
from typing import Dict
from . import helpers


def test_bad_payload_returns_400_bad_request(db, client: TestClient):
    response = helpers.send_auth_post(client=client, payload={})
    assert response.status_code == 400


def test_bad_credentials_returns_401_unauthorized(
    db,
    client: TestClient,
    base_auth_payload: Dict[str, str],
):
    base_auth_payload["email"] = "Jimmy@gmail.com"
    base_auth_payload["password"] = "123456"

    response = helpers.send_auth_post(client=client, payload=base_auth_payload)
    assert response.status_code == 401


def test_staff_user_can_login(
    db,
    client: TestClient,
    base_auth_payload: Dict[str, str],
    user_email: str,
    user_password: str,
    staff_user: User,
):
    base_auth_payload["email"] = user_email
    base_auth_payload["password"] = user_password

    response = helpers.send_auth_post(client=client, payload=base_auth_payload)
    helpers.assert_good_auth_response(response=response)


def test_non_staff_user_can_login(
    db,
    client: TestClient,
    base_auth_payload: Dict[str, str],
    user_email: str,
    user_password: str,
    non_staff_user: User,
):
    base_auth_payload["email"] = user_email
    base_auth_payload["password"] = user_password

    response = helpers.send_auth_post(client=client, payload=base_auth_payload)
    helpers.assert_good_auth_response(response=response)


def test_superuser_user_can_login(
    db,
    client: TestClient,
    base_auth_payload: Dict[str, str],
    user_email: str,
    user_password: str,
    superuser_user: User,
):
    base_auth_payload["email"] = user_email
    base_auth_payload["password"] = user_password

    response = helpers.send_auth_post(client=client, payload=base_auth_payload)
    helpers.assert_good_auth_response(response=response)
