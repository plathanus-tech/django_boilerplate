import pytest

from tests.fakes import FakePushNotificationExternalService
from users.models import User


@pytest.fixture
def push_notification_service():
    return FakePushNotificationExternalService()


@pytest.mark.django_db
@pytest.fixture
def visitor_user():
    user = User(
        email="leandrodesouzadev@gmail.com",
        full_name="Leandro de Souza",
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )
    user.set_password("password")
    user.full_clean()
    user.save()
    return user
