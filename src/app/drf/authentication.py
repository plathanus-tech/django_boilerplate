from typing import Any

from rest_framework.authentication import TokenAuthentication as DrfTokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import (
    JWTAuthentication as DrfJwtAuthentication,
)

from users.models import User
from users.services.auth import user_update_last_login_on_succesfull_api_authentication

AuthResult = tuple[User, Any] | None


def after_authenticate(auth_result: AuthResult) -> AuthResult:
    if auth_result is None:
        return None
    user, token = auth_result
    user_update_last_login_on_succesfull_api_authentication(user=user)
    return auth_result


class LastLoginAwareTokenAuthentication(DrfTokenAuthentication):
    """Normally the `TokenAuthentication` from rest framework does not updates
    the `last_login` field, this class does not changes any behavior of the rest
    framework.

    Only after the authentication is succesful check if the `last_login`
    was never updated/was not updated on the current date."""

    def authenticate(self, request):
        auth_result: tuple[User, Token] | None = super().authenticate(request)
        return after_authenticate(auth_result)


class LastLoginAwareJwtAuthentication(DrfJwtAuthentication):
    def authenticate(self, request):
        auth_result: tuple[User, str] | None = super().authenticate(request)  # type: ignore
        return after_authenticate(auth_result)
