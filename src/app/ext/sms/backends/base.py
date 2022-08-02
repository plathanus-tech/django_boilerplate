from abc import ABC, abstractmethod


class BaseSmsBackend(ABC):
    @abstractmethod
    def send(self, *, receiver: str, body: str) -> None:
        """Sends a SMS with a `body` to a `receiver` phone"""
        pass
