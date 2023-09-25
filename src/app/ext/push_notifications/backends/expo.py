import logging
from typing import Any, Iterable, Sequence, TypedDict

import requests

from app.ext.push_notifications.abc import (
    PushNotificationExternalService,
    PushReceipt,
    PushTicket,
)
from push_notifications.models import PushNotification

logger = logging.getLogger("expo_notifications")


class ExpoSinglePushResponse(TypedDict):
    data: PushTicket


class ExpoMultiplePushesResponse(TypedDict):
    data: Iterable[PushTicket]


class ExpoGetReceiptResponse(TypedDict):
    data: dict[str, PushReceipt]


class ExpoPushNotificationExternalService(PushNotificationExternalService):
    suitable_for_production = True

    # Based on: https://docs.expo.dev/push-notifications/sending-notifications/#http2-api
    _SEND_URL = "https://exp.host/--/api/v2/push/send"
    _RECEIPT_URL = "https://exp.host/--/api/v2/push/getReceipts"
    _READ_TIMEOUT = 10
    _MAX_ITEMS_PER_REQUEST = 100

    def __init__(self):
        self.s = requests.Session()

    def _push_json_data(self, push: PushNotification) -> dict[str, Any]:
        return {
            "to": push.user.notification_token,
            "title": push.title,
            "body": push.description,
            "data": push.enriched_data,
        }

    def send(self, push: PushNotification) -> PushTicket:
        logger.info(f"Sending Expo Push {push=}")
        response: requests.Response = self.s.post(
            url=self._SEND_URL,
            json=self._push_json_data(push),
            timeout=self._READ_TIMEOUT,
        )
        logger.info(f"Expo Push {response.status_code=} {response.text=}")
        data: ExpoSinglePushResponse = response.json()
        return data["data"]

    def bulk_send(self, pushes: Sequence[PushNotification]) -> dict[str, PushTicket]:
        logger.info(f"Sending expo bulk push to {len(pushes)} devices")
        tickets: dict[str, PushTicket] = {}
        for step in range(0, len(pushes), self._MAX_ITEMS_PER_REQUEST):
            next_step = step + self._MAX_ITEMS_PER_REQUEST
            step_pushes: list[PushNotification] = [push for push in pushes[step:next_step]]
            response: requests.Response = self.s.post(
                url=self._SEND_URL,
                json=[self._push_json_data(push) for push in step_pushes],
                timeout=self._READ_TIMEOUT,
            )
            logger.info(f"Expo Push {response.status_code=} {response.text=}")
            data: ExpoMultiplePushesResponse = response.json()
            for i, ticket in enumerate(data["data"]):
                tickets[str(step_pushes[i].id)] = ticket
        return tickets

    def get_receipts(self, ticket_ids: Sequence[str]) -> dict[str, PushReceipt]:
        logger.info(f"Retrieving receipts for {ticket_ids=}")

        receipts: dict[str, PushReceipt] = {}
        for step in range(0, len(ticket_ids), self._MAX_ITEMS_PER_REQUEST):
            next_step = step + self._MAX_ITEMS_PER_REQUEST
            step_ids = ticket_ids[step:next_step]
            response: requests.Response = self.s.post(url=self._RECEIPT_URL, json={"ids": step_ids})
            data: ExpoGetReceiptResponse = response.json()
            receipts.update(data["data"])
        return receipts
