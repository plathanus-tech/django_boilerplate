from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PushNotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "push_notifications"
    verbose_name = _("Push Notification")
    verbose_name_plural = _("Push Notifications")
