from datetime import datetime, timedelta
from typing import Any, Sequence

from django.utils import timezone

from app import consts
from app.ext import di
from app.ext.push_notifications.abc import (
    PushNotificationExternalService,
    PushReceipt,
    PushTicket,
)
from app.models import BaseModel
from users.models import User

from . import models


def push_notification_create(
    *,
    user: User,
    kind: consts.push_notification.Kind.kind_enum,
    title: str,
    description: str,
    data: dict[str, Any] | None = None,
    source_object: BaseModel | None = None,
) -> models.PushNotification:
    data = data or {}

    push_notification = models.PushNotification(
        user=user,
        kind=kind,
        title=title,
        description=description,
        data=data,
        status=consts.push_notification.Status.CREATED,
        source_object=source_object,
    )
    if user.notification_token is None:
        push_notification.status = consts.push_notification.Status.FAILED
        push_notification.failure_kind = consts.push_notification.FailureKind.NOT_OPTED_IN
        push_notification.failure_message = "The user has not opted-in to receive notifications"
    push_notification.full_clean()
    push_notification.save()
    return push_notification


def push_notification_handle_push_ticket(
    *,
    notification: models.PushNotification,
    ticket: PushTicket,
) -> None:
    """Handles a PushTicket, if it's ok the notification has been received by the
    service responsible to delivering the notification to the end-user, but that
    doesn't mean that the message was delivered to the end-user"""
    from . import tasks

    status = ticket["status"]
    if status not in ("ok", "error"):
        return
    if status == "ok":
        notification.push_ticket_id = ticket["id"]
        notification.status = consts.push_notification.Status.SENT
        notification.save()
        return

    notification.failure_kind = ticket["details"]["error"]
    notification.failure_message = ticket["message"]
    notification.status = consts.push_notification.Status.FAILED
    notification.save()

    tasks.push_notification_handle_delivery_failure.apply_async(
        kwargs={"notification_id": notification.id}
    )


def push_notification_handle_push_receipt(
    *, notification: models.PushNotification, receipt: PushReceipt
) -> None:
    """Handles a PushReceipt, if it's ok, the notification was delivered to the end-user
    Otherwise has failed and maybe can be retried"""
    from . import tasks

    status = receipt["status"]
    if status not in ("ok", "error"):
        return
    if status == "ok":
        notification.status = consts.push_notification.Status.DELIVERED
        notification.delivery_confirmation_received_at = timezone.now()
        notification.save()
        return

    notification.failure_kind = receipt["details"]["error"]
    notification.failure_message = receipt["message"]
    notification.status = consts.push_notification.Status.FAILED
    notification.save()
    tasks.push_notification_handle_delivery_failure.apply_async(
        kwargs={"notification_id": notification.id}
    )


@di.inject_service_at_runtime(PushNotificationExternalService)
def push_notification_send(
    *,
    notifications: Sequence[models.PushNotification],
    notification_service: PushNotificationExternalService = PushNotificationExternalService(),
) -> None:
    """Expects a sequence of PushNotification that are on the CREATED/ENQUEUED status"""
    sendable_statuses = (
        consts.push_notification.Status.CREATED,
        consts.push_notification.Status.ENQUEUED,
    )
    sendable_notifications = [n for n in notifications if n.status in sendable_statuses]
    if not sendable_notifications:
        return

    tickets = notification_service.bulk_send(pushes=sendable_notifications)
    for notification in sendable_notifications:
        ticket = tickets.get(str(notification.id), None)
        if ticket is None:
            continue
        push_notification_handle_push_ticket(notification=notification, ticket=ticket)


def push_notification_delivery_failed(notification: models.PushNotification):
    """Handles a push notification that failed when we tried to sent it to the provider.
    It expects that failure_kind is populated, meaning that is on the failed status"""
    from . import tasks

    if notification.failure_kind == consts.push_notification.FailureKind.DEVICE_NOT_REGISTERED:
        # we're recommended to not keep trying sending notifications to non-registered devices
        user: User = notification.user
        user.notification_token = None
        user.save()
        return

    if notification.failure_kind == consts.push_notification.FailureKind.MESSAGE_RATE_EXCEEDED:
        if notification.delivery_attempts > notification.MAX_DELIVERY_ATTEMPTS:
            notification.status = consts.push_notification.Status.FAILED
            notification.failure_kind = (
                consts.push_notification.FailureKind.TOO_MANY_DELIVERY_ATTEMPTS
            )
            notification.failure_message = "Too many attempts to deliver the notification failed"
            notification.save()
            return
        notification.status = consts.push_notification.Status.ENQUEUED
        notification.delivery_attempts += 1
        notification.failure_kind = None
        notification.failure_message = None
        notification.save()
        tasks.push_notification_handle_resend.apply_async(
            kwargs={"notification_id": notification.id}
        )

    # TODO: Log that we can't handle this


@di.inject_service_at_runtime(PushNotificationExternalService)
def push_notification_confirm_delivery(
    *,
    dt: datetime,
    notification_service: PushNotificationExternalService = PushNotificationExternalService(),
):
    """Tries to confirm the delivery of sent notifications that
    were created after dt - 1 days. This is called periodically by celery"""
    yesterday = dt - timedelta(days=1)
    notifications = models.PushNotification.objects.filter(
        status=consts.push_notification.Status.SENT,
        created_at__date__gte=yesterday.date(),
        push_ticket_id__isnull=False,
    ).select_related("user")
    if not notifications:
        # No need to send no tickets to the notification service
        return
    receipts = notification_service.get_receipts(
        [notification.push_ticket_id for notification in notifications]  # type: ignore
    )

    for notification in notifications:
        receipt = receipts.get(notification.push_ticket_id)  # type: ignore
        if receipt is None:
            continue
        push_notification_handle_push_receipt(
            notification=notification,
            receipt=receipt,
        )


@di.inject_service_at_runtime(PushNotificationExternalService)
def push_notification_resend_failed_notification(
    *,
    notification: models.PushNotification,
    notification_service: PushNotificationExternalService = PushNotificationExternalService(),
):
    """Tries to resend the notification that has failed to process before"""
    push_notification_send(notification_service=notification_service, notifications=[notification])


def push_notification_read(
    *, push_notification: models.PushNotification
) -> models.PushNotification:
    if push_notification.read_at is not None:
        return push_notification
    push_notification.read_at = timezone.now()
    push_notification.status = consts.push_notification.Status.READ
    push_notification.save()
    return push_notification
