from .base import BaseSmsBackend


class StdOutSmsBackend(BaseSmsBackend):
    """A backend that will print to stdout SMS notifications"""

    def send(self, *, receiver: str, body: str) -> None:
        print(f"New SMS Notification {receiver=} {body=}")
