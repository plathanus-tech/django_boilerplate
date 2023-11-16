from datetime import timedelta

import pytest
from django.utils import timezone

from users.models import User
from users.services import auth


@pytest.mark.django_db
def test_authenticate_on_inexistent_account():
    with pytest.raises(auth.InactiveOrInexistentAccount):
        auth.authenticate(username="foo", password="123")


@pytest.mark.django_db
def test_authenticate_on_inactive_account(visitor_user: User):
    visitor_user.is_active = False
    visitor_user.save()

    with pytest.raises(auth.InactiveOrInexistentAccount):
        auth.authenticate(username=visitor_user.get_username(), password="password")


@pytest.mark.django_db
def test_authenticate_on_invalid_credentials(visitor_user: User):
    assert visitor_user.check_password("foo") is False

    with pytest.raises(auth.InvalidCredentials):
        auth.authenticate(username=visitor_user.get_username(), password="foo")


@pytest.mark.django_db
def test_authenticate_valid_credentials(visitor_user: User):
    assert visitor_user.is_active
    assert visitor_user.check_password("password")
    assert visitor_user.last_login is None

    authenticated_user = auth.authenticate(
        username=visitor_user.get_username(), password="password"
    )
    assert authenticated_user == visitor_user
    assert authenticated_user.last_login is not None


@pytest.mark.django_db
def test_token_authenticate_valid_credentials(visitor_user: User):
    assert visitor_user.is_active
    assert visitor_user.check_password("password")

    # The token authenticate method is basically a proxy to the authenticate method
    # So there's no need to test all the bad cases, they're already handled above
    user, token = auth.token_authenticate(username=visitor_user.get_username(), password="password")
    assert visitor_user == user
    assert token.user_id == user.id


@pytest.mark.django_db
def test_user_updated_last_login_on_succesfull_api_authentication(visitor_user: User):
    def get_user(user: User) -> User:
        # Tricks mypy to think that the object has changed, so assert statements
        # are correctly checked, this is required because the function is modifying
        # the user object, and mypy doesn't like that
        return user

    # User has never logged in before, update last login
    assert visitor_user.last_login is None
    auth.user_update_last_login_on_succesfull_api_authentication(user=visitor_user)
    visitor_user = get_user(visitor_user)
    assert visitor_user.last_login is not None

    # User logged-in yesterday, update last login
    yesterday_user = User.objects.get(pk=visitor_user.pk)
    yesterday_user.last_login = timezone.now() - timedelta(days=1)
    auth.user_update_last_login_on_succesfull_api_authentication(user=yesterday_user)
    assert yesterday_user.last_login is not None
    assert yesterday_user.last_login.date() == timezone.now().date()

    # user logged in today, no updates
    last_login = timezone.now().replace(hour=12)
    visitor_user.last_login = last_login
    auth.user_update_last_login_on_succesfull_api_authentication(user=visitor_user)
    assert visitor_user.last_login == last_login
