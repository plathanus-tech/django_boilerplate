from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, TypedDict


class NotificationData(TypedDict, total=False):
    id: int
    createdAt: str
    viewedAt: str
    timeSinceCreated: str
    type: str
    obj: Any


@dataclass
class PushNotification:
    to: str
    title: str
    body: str
    data: NotificationData


class PushNotificationService(ABC):
    @abstractmethod
    def send(self, push: PushNotification) -> None:
        raise NotImplementedError("This method should be implemented on the child class")

    @abstractmethod
    def bulk_send(self, notifications: List[PushNotification]) -> None:
        raise NotImplementedError("This method should be implemented on the child class")
