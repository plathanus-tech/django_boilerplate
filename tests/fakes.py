from typing import List

from app.ext.push_notifications.base import PushNotification, PushNotificationService


class FakePushNotificationService(PushNotificationService):

    calls: List[PushNotification]

    def __init__(self):
        self.calls = []

    def send(self, push: PushNotification) -> None:
        if not self.calls:
            self.calls = []
        self.calls.append(push)

    def bulk_send(self, notifications: List[PushNotification]) -> None:
        self.calls.extend(notifications)
