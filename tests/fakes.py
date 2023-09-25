import uuid
from typing import Iterable

from app.ext.push_notifications.abc import (
    PushNotificationExternalService,
    PushReceipt,
    PushTicket,
)
from push_notifications.models import PushNotification


class FakePushNotificationExternalService(PushNotificationExternalService):
    def __init__(
        self, result_ticket: PushTicket | None = None, receipt_result: PushReceipt | None = None
    ):
        self.result_ticket = result_ticket or {"status": "ok", "id": str(uuid.uuid4())}
        self.receipt_result = receipt_result or {"status": "ok", "id": str(uuid.uuid4())}

    def send(self, push: PushNotification) -> PushTicket:
        return self.result_ticket

    def bulk_send(self, pushes: Iterable[PushNotification]) -> dict[str, PushTicket]:
        return {str(push.id): self.result_ticket for push in pushes}

    def get_receipts(self, ticket_ids: Iterable[str]) -> dict[str, PushReceipt]:
        return {ticket_id: self.receipt_result for ticket_id in ticket_ids}
