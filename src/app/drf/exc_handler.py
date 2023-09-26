import logging
from typing import Any, TypeVar

from django.core import exceptions as django_exceptions
from django.http import Http404 as DjangoHttp404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

from app.exceptions import ApplicationError

ExceptionLike = TypeVar(
    "ExceptionLike",
    ApplicationError,
    django_exceptions.ValidationError,
    DjangoHttp404,
    django_exceptions.PermissionDenied,
    exceptions.APIException,
)


logger = logging.getLogger("api.bad_requests")


def custom_exception_handler(exc: ExceptionLike, ctx: dict[str, Any]):
    """
    {
        "kind": "ErrorClassName",
        "message": "Error message",
        "extra": {}
    }
    """

    if isinstance(exc, django_exceptions.ValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, DjangoHttp404):
        exc = exceptions.NotFound()

    if isinstance(exc, django_exceptions.PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        logger.debug(f"Got exception raised {exc=}")
        if isinstance(exc, ApplicationError):
            data = {"kind": exc.__class__.__name__, "message": exc.message, "extra": exc.extra}
            return Response(data, status=exc.http_status_code)
        return None

    if isinstance(exc.detail, (list, dict)):  # type: ignore
        response.data = {"detail": response.data}

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {"fields": response.data["detail"]}
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]
    response.data["kind"] = exc.__class__.__name__

    logger.debug(f"Captured some other exception {response.data=}")
    return response
