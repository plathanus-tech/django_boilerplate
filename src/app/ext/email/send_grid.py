import logging
from typing import Sequence

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.base import BaseEmailBackend
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


class SendGridEmailBackend(BaseEmailBackend):
    client: SendGridAPIClient
    fail_silently: bool

    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        super().__init__(fail_silently, **kwargs)
        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        logger.info(f"Received {len(email_messages)} email_messages to send")

        succeeded_messages = 0
        for email in email_messages:
            mail = Mail(
                from_email=email.from_email,
                to_emails=email.to,
                subject=email.subject,
                plain_text_content=email.body,
            )
            try:
                logger.info(f"Tryng to send request to sendgrid {mail=}")
                response = self.client.send(mail)
            except Exception as e:
                if not self.fail_silently:
                    logger.exception("Failed to send a email")
                    raise e
                logger.warning("Failed to send a email, but fail_silently was set. Ignoring")
                continue

            logger.info(f"Succesfully sent the request to sendgrid. {response.status_code=}")
            if response.status_code == 200:
                succeeded_messages += 1

        logger.info(f"Finished {len(email_messages)=}. {succeeded_messages=}")
        return succeeded_messages
