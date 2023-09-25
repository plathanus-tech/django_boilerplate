import pytest
from pytest_mock import MockerFixture

from app import consts
from push_notifications import models, services
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
def test_push_notification_handle_push_receipt_succeeded(
    push_notification: models.PushNotification,
):
    """When we receive a push receipt back, and it's with a ok status,
    this means that the message was sucessfully delivered to the end-user"""

    services.push_notification_handle_push_receipt(
        notification=push_notification, receipt={"status": "ok"}
    )
    push_notification.refresh_from_db()
    assert push_notification.status == consts.push_notification.Status.DELIVERED
    assert push_notification.delivery_confirmation_received_at is not None


@pytest.mark.django_db
def test_push_notification_handle_push_receipt_failed(
    push_notification: models.PushNotification, mocker: MockerFixture
):
    """When we receive a push ticket back, and it's with a error status,
    this means that the message has failed to be sent to the provider, this should
    update the status with the ticket info, this means that the message couldn't be
    delivered or sent to the provider, either way we dispatch a task to handle this
    failure"""

    handle_delivery_failure_task = mocker.patch(
        "push_notifications.tasks.push_notification_handle_delivery_failure.apply_async"
    )
    services.push_notification_handle_push_receipt(
        notification=push_notification,
        receipt={
            "status": "error",
            "message": "Oops, failed to communicate",
            "details": {"error": "MessageTooBig"},
        },
    )
    push_notification.refresh_from_db()
    assert push_notification.status == consts.push_notification.Status.FAILED
    assert push_notification.failure_kind == consts.push_notification.FailureKind.MESSAGE_TOO_BIG
    assert push_notification.failure_message == "Oops, failed to communicate"

    handle_delivery_failure_task.assert_called_once_with(
        kwargs={"notification_id": push_notification.id}
    )
