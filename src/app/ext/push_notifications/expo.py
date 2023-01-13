import logging
from typing import List

import requests
from django.conf import settings

from .base import PushNotification, PushNotificationService

logger = logging.getLogger("expo_notifications")


class ExpoPushNotificationService(PushNotificationService):
    # Based on: https://docs.expo.dev/push-notifications/sending-notifications/#http2-api
    _URL = "https://exp.host/--/api/v2/push/send"

    def send(self, push: PushNotification) -> None:
        logger.info(f"Sending Expo Push {push=}")
        response: requests.Response = requests.post(
            url=self._URL,
            json={
                "to": push.to,
                "title": push.title,
                "body": push.body,
                "data": push.data,
            },
        )
        log = logger.info
        if not response.ok:
            log = logger.error
        log(f"Expo Push {response.status_code=} {response.text=}")

    def bulk_send(self, notifications: List[PushNotification]) -> None:
        logger.info(f"Sending expo bulk push to {len(notifications)} devices")
        maximum_notifications_per_request = 100
        for step in range(0, len(notifications), maximum_notifications_per_request):
            next_step = step + maximum_notifications_per_request
            response: requests.Response = requests.post(
                url=self._URL,
                json=notifications[step:next_step],
            )
            log = logger.info
            if not response.ok:
                log = logger.error
            log(f"Expo Push {response.status_code=} {response.text=}")
