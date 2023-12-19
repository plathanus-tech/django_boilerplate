import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

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
    content_type = ContentType.objects.get_for_model(User)  # type: ignore
    permissions = Permission.objects.filter(
        content_type=content_type,
    )
    user.user_permissions.set(permissions)
    timezone.activate(user.time_zone)
    yield user


@pytest.fixture(autouse=True)
def set_log_events_context():
    from app.logging.utils import _log_events

    _log_events.set([])
