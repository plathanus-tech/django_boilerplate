from typing import Type

from django.conf import settings
from django.utils.module_loading import import_string

from .backends.base import BaseSmsBackend


def send_sms(*, receiver: str, body: str) -> None:
    """Sends a SMS using a settings defined Backend"""
    klass: Type[BaseSmsBackend] = import_string(settings.SMS_BACKEND)
    backend = klass()

    backend.send(receiver=receiver, body=body)
