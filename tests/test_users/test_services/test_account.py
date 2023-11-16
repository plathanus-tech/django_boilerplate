import pytest

from users.models import User
from users.services import account


@pytest.mark.django_db
def test_user_delete_account_changes_email(visitor_user: User):
    previous_email = visitor_user.email

    account.user_delete_account(visitor_user)

    deleted_account = User.objects.get(id=visitor_user.id)
    assert deleted_account.is_active is False
    assert deleted_account.email != previous_email

    assert User.objects.filter(email=previous_email).exists() is False
