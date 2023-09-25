from typing import Literal

from django.utils.translation import gettext_lazy as _


class MaxSize:
    # Altough IOS users have limitations, they are bigger than android users
    TITLE_MAX_SIZE_ANDROID = 65
    DESCRIPTION_MAX_SIZE_ANDROID = 240


class Status:
    CREATED = "c"
    ENQUEUED = "e"
    SENT = "s"
    DELIVERED = "d"
    READ = "r"
    FAILED = "f"

    choices = (
        (CREATED, _("Created")),
        (ENQUEUED, _("Enqueued")),
        (SENT, _("Sent")),
        (DELIVERED, _("Delivered")),
        (READ, _("Read")),
        (FAILED, _("Failed")),
    )


class FailureKind:
    # These kind values matches expo notification errors
    DEVICE_NOT_REGISTERED = "DeviceNotRegistered"
    MESSAGE_TOO_BIG = "MessageTooBig"
    MESSAGE_RATE_EXCEEDED = "MessageRateExceeded"
    MISMATCH_SENDER_ID = "MismatchSenderId"
    INVALID_CREDENTIALS = "InvalidCredentials"

    # These kinds are custom
    NOT_OPTED_IN = "NotOptedIn"
    TOO_MANY_DELIVERY_ATTEMPTS = "TooManyDeliveryAttempts"

    choices = (
        (DEVICE_NOT_REGISTERED, _("Device not registered")),
        (MESSAGE_TOO_BIG, _("Message too big")),
        (MESSAGE_RATE_EXCEEDED, _("Message rate exceeded")),
        (MISMATCH_SENDER_ID, _("Mismatch sender ID")),
        (INVALID_CREDENTIALS, _("Invalid credentials")),
        (NOT_OPTED_IN, _("Not opted-in")),
        (TOO_MANY_DELIVERY_ATTEMPTS, _("Too many delivery attempts")),
    )


class Kind:
    """Define here all the Kind of push notifications this application may sent"""

    INTERNAL_COMMUNICATION: Literal["int_comm"] = "int_comm"

    choices = ((INTERNAL_COMMUNICATION, _("Internal communication")),)
    kind_enum = Literal["int_comm"]
