from django.conf import settings

from app.ext.abc import ExternalService


def sms_external_service_loader() -> "SMSExternalService":
    from .backends.stdout import DevStdOutSMSExternalService
    from .backends.twilio import TwilioSMSExternalService

    available_backends = {
        "dev.stdout": DevStdOutSMSExternalService,
        "twilio": TwilioSMSExternalService,
    }
    backend_class = available_backends[settings.SMS_EXTERNAL_SERVICE_BACKEND]
    return backend_class()


class SMSExternalService(ExternalService):
    service_loader = sms_external_service_loader

    def send(self, *, receiver: str, body: str) -> None:
        """Sends a SMS with a `body` to a `receiver` phone"""
        raise NotImplementedError("Missing implementation for send")
