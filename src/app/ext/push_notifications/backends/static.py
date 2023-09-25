import uuid
from typing import Sequence

from app.ext.push_notifications.abc import (
    PushNotificationExternalService,
    PushReceipt,
    PushTicket,
)
from push_notifications.models import PushNotification


class StaticPushNotificationExternalService(PushNotificationExternalService):
    """This service always returns a succeeded push ticket or recipe"""

    suitable_for_production = False

    def _ok_push_ticket(self) -> PushTicket:
        return {"status": "ok", "id": str(uuid.uuid4())}

    def send(self, push: PushNotification) -> PushTicket:
        return self._ok_push_ticket()

    def bulk_send(self, pushes: Sequence[PushNotification]) -> dict[str, PushTicket]:
        return {str(push.id): self._ok_push_ticket() for push in pushes}

    def get_receipts(self, ticket_ids: Sequence[str]) -> dict[str, PushReceipt]:
        return {ticket_id: self._ok_push_ticket() for ticket_id in ticket_ids}
