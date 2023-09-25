import pytest
from pytest_mock import MockerFixture

from app import consts
from push_notifications import models, services
from tests.fakes import FakePushNotificationExternalService
from users.models import User


@pytest.fixture
def push_notification(visitor_user: User) -> models.PushNotification:
    if visitor_user.notification_token is None:
        visitor_user.notification_token = "foo"
        visitor_user.save()

    return services.push_notification_create(
        user=visitor_user,
        kind=consts.push_notification.Kind.INTERNAL_COMMUNICATION,
        title="Hey you, yes you!",
        description="We have a new vaccine available",
        data={"foo": "bar"},
    )


@pytest.mark.django_db
def test_push_notification_send_doesnt_send_on_failed_status(
    push_notification: models.PushNotification,
    push_notification_service: FakePushNotificationExternalService,
    mocker: MockerFixture,
):
    """When we try to send a notification, it may be on a failed status directly after it's
    created, in that case we don't want to send that over to the notification service"""

    push_notification.status = consts.push_notification.Status.FAILED
    push_notification.save()

    bulk_send_spy = mocker.spy(push_notification_service, "bulk_send")
    services.push_notification_send(
        notification_service=push_notification_service, notifications=[push_notification]
    )
    bulk_send_spy.assert_not_called()


@pytest.mark.django_db
def test_push_notification_send_sends_when_on_expected_status(
    push_notification: models.PushNotification,
    push_notification_service: FakePushNotificationExternalService,
):
    """When we try to send a push notification and it's on an ok status, then we should
    send them over the integration service, then with the ticket we received back the notification
    status should be updated, we're not testing the ticket error case here, because that is already
    tested on the push_notification_handle_push_ticket already"""

    assert push_notification.status == consts.push_notification.Status.CREATED
    assert push_notification_service.result_ticket["status"] == "ok"
    services.push_notification_send(
        notification_service=push_notification_service, notifications=[push_notification]
    )
    push_notification.refresh_from_db()
    assert push_notification.status == consts.push_notification.Status.SENT
    assert str(push_notification.push_ticket_id) == push_notification_service.result_ticket["id"]
