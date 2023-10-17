import structlog
from django.conf import settings
from django.http import HttpRequest

from app import services
from app.logging.utils import _log_events

from .base import BaseMiddleware


class LogContextMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest):
        _log_events.set([])
        if request.user.is_authenticated:
            structlog.contextvars.bind_contextvars(user_id=request.user.id)
        return self.get_response(request)

    def process_exception(self, request, exception):
        if settings.SEND_ERROR_REPORT_ON_FAILURES:
            services.send_request_error_report(request=request, exception=exception)
