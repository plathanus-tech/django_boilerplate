from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from app.exceptions import ApplicationError
from users.models import User


class InactiveOrInexistentAccount(ApplicationError):
    http_status_code = 401
    error_message = _("The '{username}' account was not found or is inactive")


class InvalidCredentials(ApplicationError):
    http_status_code = 401
    error_message = _("Invalid password for '{username}' account")


def authenticate(*, username, password) -> User:
    user = User.objects.filter(**{User.USERNAME_FIELD: username}).first()
    if user is None:
        raise InactiveOrInexistentAccount(
            message_format_kwargs={"username": username},
            field_errors={"username": _("Please pick another account")},
        )
    if not user.check_password(password):
        raise InvalidCredentials(
            message_format_kwargs={"username": username},
            field_errors={"username": _("Password mismatch, passwords are case-sensitive")},
        )
    user_check_is_valid(user=user)
    user_authenticated_succesfully(user=user)
    return user


def user_check_is_valid(*, user: User):
    if user.is_active is False:
        raise InactiveOrInexistentAccount(
            message_format_kwargs={"username": user.get_username()},
            field_errors={"username": _("Please pick another account")},
        )


def user_authenticated_succesfully(user: User):
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])


def token_authenticate(*, username, password) -> tuple[User, Token]:
    user = authenticate(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    user.auth_token = token  # sets accessor, so no additional queries are required
    return user, token


def user_update_last_login_on_succesfull_api_authentication(user: User):
    """After the user is logged-in, he probably won't be authenticating very often
    because of a static token or long-lived JWT tokens, in that case the last_login
    field would not reflect the last time that the user has accessed the application.
    But we don't do this on every single interaction to not overhead the database"""
    if user.last_login is None or user.last_login.date() < timezone.now().date():
        user_authenticated_succesfully(user=user)
