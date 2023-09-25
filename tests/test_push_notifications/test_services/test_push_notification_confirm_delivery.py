import uuid

import pytest
from django.utils import timezone

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
def test_push_notification_confirm_delivery_updates_status_to_delivered_when_receipt_is_received(
    push_notification: models.PushNotification,
    push_notification_service: FakePushNotificationExternalService,
):
    """When we try to confirm the delivery of a notification, and the service returns us the receipt
    that the notification was delivered, we should update the status of the notification to delivered
    """

    assert push_notification_service.receipt_result["status"] == "ok"

    push_notification.push_ticket_id = uuid.uuid4()
    push_notification.status = consts.push_notification.Status.SENT
    push_notification.save()

    services.push_notification_confirm_delivery(
        notification_service=push_notification_service, dt=timezone.now()
    )
    push_notification.refresh_from_db()

    assert push_notification.status == consts.push_notification.Status.DELIVERED
    assert push_notification.delivery_confirmation_received_at is not None
