from app.ext.sms.abc import SMSExternalService


class DevStdOutSMSExternalService(SMSExternalService):
    """A backend that will print to stdout SMS notifications"""

    suitable_for_production = False

    def send(self, *, receiver: str, body: str) -> None:
        print(f"New SMS Notification {receiver=} {body=}")
