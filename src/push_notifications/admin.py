from typing import Any

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app import consts
from app.admin.mixins import ReadOnlyAdminMixin
from push_notifications import models


@admin.register(models.PushNotification)
class PushNotificationAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "kind",
        "status",
        "title_abbreviation",
        "created_at",
        "read_at",
    )
    list_filter = (
        "kind",
        "status",
        "created_at",
        "read_at",
    )
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    list_select_related = ("user",)
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "kind",
                    "title",
                    "description",
                    "user",
                    "source_object",
                    "status",
                    "created_at",
                    "last_updated_at",
                )
            },
        ),
    ]

    @admin.display(description=_("Title"))
    def title_abbreviation(self, obj: models.PushNotification):
        suffix = "..." if len(obj.title) > 30 else ""
        return f"{obj.title[:27]}{suffix}"

    def get_fieldsets(self, request, obj: models.PushNotification | None = None):
        if obj is None:
            return self.fieldsets
        fieldsets: Any = self.fieldsets.copy()
        if obj.status == consts.push_notification.Status.FAILED:
            fieldsets.append(
                (
                    _("Failure reason"),
                    {
                        "fields": (
                            "push_ticket_id",
                            "delivery_attempts",
                            "failure_kind",
                            "failure_message",
                        )
                    },
                )
            )
        if obj.status == consts.push_notification.Status.DELIVERED:
            fieldsets.append(
                (_("Delivery"), {"fields": ("delivery_confirmation_received_at", "read_at")}),
            )
        if obj.data:
            fieldsets.append((_("Metadata"), {"fields": ("data",)}))
        return fieldsets
