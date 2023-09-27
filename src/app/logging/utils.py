from contextvars import ContextVar
from typing import Any

from .types import BoundLogCollector, StructLogger

# This context-var is used by middlewares/signals
_log_events: ContextVar[list[dict[str, Any]]] = ContextVar("_log_events")


def get_logger(name: str, **initial_context) -> StructLogger:
    # import this here to not polute the import auto-complete
    import structlog
    from celery.utils.log import get_task_logger

    logger = structlog.wrap_logger(
        get_task_logger(name),
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.filter_by_level,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=BoundLogCollector,  # type: ignore
        **initial_context,
    )
    return logger
