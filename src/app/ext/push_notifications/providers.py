from typing import Dict, Type, Union

from django.conf import settings

from .base import PushNotificationService
from .expo import ExpoPushNotificationService

services: Dict[str, Union[Type[PushNotificationService], PushNotificationService]] = {
    "expo": ExpoPushNotificationService
}


def get_push_notification_service_for_provider() -> PushNotificationService:
    Service = services[settings.PUSH_NOTIFICATION_SERVICE_ADAPTER]
    if callable(Service):
        return Service()
    return Service
