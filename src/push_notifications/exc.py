from django.utils.translation import gettext_lazy as _

from app.exceptions import ApplicationError


class UnableToSendPushNotification(ApplicationError):
    pass


class InvalidNotificationToken(ApplicationError):
    error_message = _("Invalid notification token, {reason}")
