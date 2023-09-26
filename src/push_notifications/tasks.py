import uuid

from django.utils.translation import gettext as _

from app.celery.decorators import BaseTask, task

from . import models, services


@task()
def push_notification_handle_delivery_failure(notification_id: int):
    notification = models.PushNotification.objects.get(pk=notification_id)
    services.push_notification_delivery_failed(notification=notification)


@task()
def push_notification_handle_resend(notification_id: int):
    notification = models.PushNotification.objects.get(pk=notification_id)
    services.push_notification_send(notifications=[notification])


@task(bind=True)
def push_notification_confirm_delivery_periodically(self: BaseTask):
    services.push_notification_confirm_delivery(
        dt=self.scheduled_at,
    )
