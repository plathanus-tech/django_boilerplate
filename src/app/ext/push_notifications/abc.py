from typing import Literal, Sequence, TypedDict

from django.conf import settings

from app.ext.abc import ExternalService
from push_notifications.models import PushNotification


class ErrorDetail(TypedDict):
    error: Literal[
        "DeviceNotRegistered",
        "MessageTooBig",
        "MessageRateExceeded",
        "MismatchSenderId",
        "InvalidCredentials",
    ]


class PushTicket(TypedDict, total=False):
    """A ticket is a receive confirmation from the provider"""

    id: str
    status: Literal["ok", "error"]
    message: str
    details: ErrorDetail


class PushReceipt(PushTicket):
    """A receipt is a delivery confirmation from the provider"""

    pass


def push_notification_external_service_loader() -> "PushNotificationExternalService":
    from .backends.expo import ExpoPushNotificationExternalService
    from .backends.static import StaticPushNotificationExternalService

    backends = {
        "expo": ExpoPushNotificationExternalService,
        "dev.static": StaticPushNotificationExternalService,
    }
    return backends[settings.PUSH_NOTIFICATION_EXTERNAL_SERVICE_BACKEND]()


class PushNotificationExternalService(ExternalService):
    service_loader = push_notification_external_service_loader

    def send(self, push: PushNotification) -> PushTicket:
        raise NotImplementedError("Missing implementation for method 'send'")

    def bulk_send(self, pushes: Sequence[PushNotification]) -> dict[str, PushTicket]:
        raise NotImplementedError("Missing implementation for method 'bulk_send'")

    def get_receipts(self, ticket_ids: Sequence[str]) -> dict[str, PushReceipt]:
        raise NotImplementedError("Missing implementation for method 'get_receipts'")
