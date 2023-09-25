from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _

from app import consts
from app.models import AutoTimeStampModel


class PushNotification(AutoTimeStampModel):
    MAX_DELIVERY_ATTEMPTS = 3

    user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        verbose_name=_("user"),
        related_name="push_notifications",
    )
    source_content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    source_object_id = models.IntegerField(
        null=True,
        blank=True,
    )
    source_object = GenericForeignKey(
        ct_field="source_content_type",
        fk_field="source_object_id",
    )
    kind = models.CharField(
        verbose_name=_("kind"),
        help_text=_("The kind of notification"),
        choices=consts.push_notification.Kind.choices,
        max_length=16,
    )
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("This is the text that shows on the top of the notification"),
        max_length=consts.push_notification.MaxSize.TITLE_MAX_SIZE_ANDROID,
    )
    description = models.CharField(
        verbose_name=_("description"),
        help_text=_("This is the text that contains the details of the notification"),
        max_length=consts.push_notification.MaxSize.DESCRIPTION_MAX_SIZE_ANDROID,
    )
    data = models.JSONField(
        verbose_name=_("additional data"),
        help_text=_("The additional data that is sent with the notification"),
        blank=True,
    )
    status = models.CharField(
        verbose_name=_("status"),
        help_text=_("The current status of this notification"),
        choices=consts.push_notification.Status.choices,
        max_length=1,
    )
    push_ticket_id = models.CharField(
        verbose_name=_("receipt ID"),
        help_text=_(
            "The notification service ID for this notification, "
            "with this receipt ID we can check if the message was delivered"
        ),
        null=True,
        blank=True,
        max_length=36,
    )
    delivery_attempts = models.SmallIntegerField(
        verbose_name=_("delivery attempts"),
        help_text=_("How many times we tried to deliver this notification"),
        default=1,
        blank=True,
    )
    failure_kind = models.CharField(
        verbose_name=_("failure kind"),
        help_text=_("When the notification fails this was the reason provided"),
        max_length=32,
        choices=consts.push_notification.FailureKind.choices,
        null=True,
        blank=True,
    )
    failure_message = models.CharField(
        verbose_name=_("failure message"),
        help_text=_("The message provided of the cause of the failure"),
        null=True,
        blank=True,
        max_length=256,
    )
    read_at = models.DateTimeField(
        verbose_name=_("read at"),
        help_text=_("The exact time that this notification was marked as read by the end-user"),
        null=True,
        blank=True,
    )
    delivery_confirmation_received_at = models.DateTimeField(
        verbose_name=_("delivery confirmation received at"),
        help_text=_(
            "When the provider of this notification confirmed the delivery of this notification"
        ),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("push notification")
        verbose_name_plural = _("push notifications")

    def __str__(self):
        return self.title

    @property
    def enriched_data(self):
        return {
            "id": self.id,
            "createdAt": str(self.created_at),
            "readAt": str(self.read_at),
            "timeSinceCreated": timesince(self.created_at),
            "kind": self.kind,
            "meta": self.data,
        }
