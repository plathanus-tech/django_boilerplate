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
def test_push_notification_delivery_failed_removes_notification_when_device_is_not_registered(
    push_notification: models.PushNotification,
):
    """When a notification failed to be delivered due to the device (notification token) is
    not registered on the provider, we are advised to no keep trying to send notifications
    to them, so we should remove the bad notification token from the user"""

    user: User = push_notification.user
    assert user.notification_token is not None
    # on a normal scenario the below information would be populated from the ticket or the receipt
    # that we got back when we tried to send this notification, but here for simplicity we're
    # setting them manually
    push_notification.status = consts.push_notification.Status.FAILED
    push_notification.failure_kind = consts.push_notification.FailureKind.DEVICE_NOT_REGISTERED
    push_notification.save()

    services.push_notification_delivery_failed(notification=push_notification)
    push_notification.refresh_from_db()

    # We expect that this values do not change
    assert push_notification.status == consts.push_notification.Status.FAILED
    assert (
        push_notification.failure_kind == consts.push_notification.FailureKind.DEVICE_NOT_REGISTERED
    )

    # now the user must have their notification token removed
    user.refresh_from_db()
    assert user.notification_token is None, "Notification token was not removed from user"


@pytest.mark.django_db
def test_push_notification_delivery_failed_dispatches_a_resend_task_when_failure_kind_is_message_rate_exceeded(
    push_notification: models.PushNotification,
    mocker: MockerFixture,
):
    """When a notification failed to be delivered due to the message rate being exceeded, we should
    try resend this notification a few times before giving up"""

    # on a normal scenario the below information would be populated from the ticket or the receipt
    # that we got back when we tried to send this notification, but here for simplicity we're
    # setting them manually
    push_notification.status = consts.push_notification.Status.FAILED
    push_notification.failure_kind = consts.push_notification.FailureKind.MESSAGE_RATE_EXCEEDED
    push_notification.failure_message = "Too many requests being sent"
    push_notification.delivery_attempts = 1
    push_notification.save()

    resend_task = mocker.patch(
        "push_notifications.tasks.push_notification_handle_resend.apply_async"
    )
    services.push_notification_delivery_failed(push_notification)
    resend_task.assert_called_once_with(kwargs={"notification_id": push_notification.id})

    # we're not using refresh_from_db because mypy complains on asserts
    notification = models.PushNotification.objects.get(pk=push_notification.pk)

    # Now the notification should be enqueued again, and the failure fields should be removed
    assert notification.status == consts.push_notification.Status.ENQUEUED
    assert notification.failure_kind is None
    assert notification.failure_message is None
    # also, the delivery attempts should be increased by 1
    assert notification.delivery_attempts == 2


@pytest.mark.django_db
def test_push_notification_delivery_failed_doesnt_dispatches_a_resend_task_after_the_max_retries(
    push_notification: models.PushNotification, mocker: MockerFixture
):
    """When a notification was already retried a few times, we don't want it to keep retrying
    infinitely, it should fail with too many attempts"""

    # on a normal scenario the below information would be populated from the ticket or the receipt
    # that we got back when we tried to send this notification, but here for simplicity we're
    # setting them manually
    push_notification.status = consts.push_notification.Status.FAILED
    push_notification.failure_kind = consts.push_notification.FailureKind.MESSAGE_RATE_EXCEEDED
    push_notification.failure_message = "Too many requests being sent"
    push_notification.delivery_attempts = models.PushNotification.MAX_DELIVERY_ATTEMPTS + 1
    push_notification.save()

    resend_task = mocker.patch(
        "push_notifications.tasks.push_notification_handle_resend.apply_async"
    )
    services.push_notification_delivery_failed(push_notification)
    resend_task.assert_not_called()

    # now the notification should be failed with failure_kind of max attempts
    # we're not using refresh_from_db because mypy complains on asserts
    notification = models.PushNotification.objects.get(pk=push_notification.pk)

    # Now the notification should be enqueued again, and the failure fields should be removed
    assert notification.status == consts.push_notification.Status.FAILED
    assert (
        notification.failure_kind == consts.push_notification.FailureKind.TOO_MANY_DELIVERY_ATTEMPTS
    )
    assert notification.failure_message is not None
