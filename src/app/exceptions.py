from typing import TYPE_CHECKING, Any, Union

from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from django_stubs_ext import StrPromise

from .consts import http


class ApplicationError(Exception):
    http_status_code: int = http.HttpStatusCode.HTTP_400_BAD_REQUEST
    error_message: Union[str, "StrPromise"] = _("Unexpected failure")

    def __init__(
        self,
        message_format_kwargs: dict[str, Any] | None = None,
        field_errors: dict[str, Any] | None = None,
        **extra,
    ):
        message_format_kwargs = message_format_kwargs or {}
        self.message = self.error_message.format(**message_format_kwargs)
        super().__init__(self.message)

        self.extra = {
            "fields": field_errors or {},
            **extra,
        }


class InsufficientPermissions(ApplicationError):
    http_status_code: int = http.HttpStatusCode.HTTP_403_FORBIDDEN
    error_message = _("Insufficient permissions")
