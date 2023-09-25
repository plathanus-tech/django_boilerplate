import logging

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

from app.ext.sms.abc import SMSExternalService

logger = logging.getLogger(__name__)


class TwilioSMSExternalService(SMSExternalService):
    suitable_for_production = True

    def __init__(self):
        self.SID = settings.TWILIO_ACCOUNT_SID
        self.URL = f"https://api.twilio.com/2010-04-01/Accounts/{self.SID}/Messages.json"
        self.TOKEN = settings.TWILIO_AUTH_TOKEN
        self.PHONE = settings.TWILIO_SERVICE_PHONE

    def send(self, *, receiver: str, body: str) -> None:
        logger.info(f"Starting new Twilio SMS request. {receiver=} {body=}")
        response = requests.post(
            url=self.URL,
            data={"Body": body, "From": self.PHONE, "To": receiver},
            auth=HTTPBasicAuth(self.SID, self.TOKEN),
            timeout=10,
        )
        log_func = logger.info
        if not response.ok:
            log_func = logger.error
        log_func(f"Finished Twilio SMS request. {response.status_code=} {response.text=}")
