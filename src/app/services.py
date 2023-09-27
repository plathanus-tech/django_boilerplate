import json
import traceback
from io import StringIO

from billiard.einfo import ExceptionInfo
from django.conf import settings
from django.http import HttpRequest
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from app.celery.decorators import BaseTask
from app.ext import di
from app.ext.messaging.abc import (
    EmbedFile,
    Message,
    MessagingExternalService,
    TextBold,
    TextCodeInline,
    TextItalic,
)
from app.logging.utils import _log_events


def _get_embed_files(formatted_traceback: str | None = None) -> list[EmbedFile]:
    tb: str = formatted_traceback or traceback.format_exc()
    traceback_file = EmbedFile(io=StringIO(tb), filename="traceback.py", content_type="text/py")
    embed_files = [traceback_file]
    try:
        logs = _log_events.get()
    except LookupError:
        logs = []

    if logs:
        embed_files.append(
            EmbedFile(
                io=StringIO(json.dumps(logs, ensure_ascii=False, indent=2)),
                filename="logs.json",
                content_type="application/json",
            )
        )
    return embed_files


@di.inject_service_at_runtime(MessagingExternalService)
def send_request_error_report(
    *,
    request: HttpRequest,
    exception: Exception,
    messaging_service: MessagingExternalService = MessagingExternalService(),
):
    """Sends a error report over a messaging service.
    This is triggered after a request fails, by a middleware.
    This report is only sent if `DEBUG=False`.
    """
    if settings.DEBUG:
        return

    with translation.override(settings.SEND_ERROR_REPORT_ON_LANGUAGE, deactivate=True):
        message = Message(
            TextBold(_("Request failed at"))
            + ": "
            + TextCodeInline(f"{request.method} {request.path}"),
            TextBold(_("Exception class")) + ": " + TextCodeInline(exception.__class__.__name__),
            TextItalic(_("More information available on the attached logs/traceback")),
        )
        receiver = settings.ERROR_REPORT_REQUEST_CHANNEL_ID
        embed_files = _get_embed_files()
        messaging_service.send(to=receiver, message=message, files=embed_files)


@di.inject_service_at_runtime(MessagingExternalService)
def send_task_error_report(
    *,
    task: BaseTask,
    exception: Exception,
    einfo: ExceptionInfo,
    messaging_service: MessagingExternalService = MessagingExternalService(),
):
    """Sends a error report over a messaging service.
    This is triggered after a celery task fails, by a signal.
    This report is only sent if `DEBUG=False`.
    """
    if settings.DEBUG:
        return

    with translation.override(settings.SEND_ERROR_REPORT_ON_LANGUAGE, deactivate=True):
        message = Message(
            TextBold(_("Task failed")) + ": " + TextCodeInline(task.name),
            TextBold(_("Task id")) + ": " + TextCodeInline(task.request.id),
            TextBold(_("Task args")) + ": " + TextCodeInline(task.request.args),
            TextBold(_("Task kwargs")) + ": " + TextCodeInline(task.request.kwargs),
            TextBold(_("Exception class")) + ": " + TextCodeInline(exception.__class__.__name__),
            TextItalic(_("More information available on the attached logs/traceback")),
        )
        receiver = settings.ERROR_REPORT_TASK_CHANNEL_ID
        embed_files = _get_embed_files(formatted_traceback=einfo.traceback)
        messaging_service.send(to=receiver, message=message, files=embed_files)
