from typing import Protocol, Self

import structlog
from django.utils import timezone


class StructLogger(Protocol):
    events: list[str]

    def bind(self, **new_values) -> Self:
        ...

    def new(self, **new_values) -> Self:
        ...

    def unbind(self, **values) -> Self:
        ...

    def debug(self, msg, *args, **kwargs) -> None:
        ...

    def info(self, msg, *args, **kwargs) -> None:
        ...

    def warning(self, msg, *args, **kwargs) -> None:
        ...

    def error(self, msg, *args, **kwargs) -> None:
        ...

    def critical(self, msg, *args, **kwargs) -> None:
        ...

    def exception(self, msg, *args, **kwargs) -> None:
        ...


class BoundLogCollector(structlog.stdlib.BoundLogger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def collect_and_proxy_to_logger(self, method_name: str, event: str, *event_args, **event_kw):
        from .utils import _log_events

        try:
            args, kw = self._process_event(method_name, event, event_kw)
            event_data = args[0].copy()
            getattr(self._logger, method_name)(*args, **kw)
        except structlog.DropEvent:
            return None
        data = {
            "timestamp": timezone.now().isoformat(),
            "context": self._context,
            **event_data,
        }
        _log_events.get().append(data)

    def debug(self, event=None, *args, **kwargs):
        return self.collect_and_proxy_to_logger("debug", event, *args, **kwargs)

    def info(self, event=None, *args, **kwargs):
        return self.collect_and_proxy_to_logger("info", event, *args, **kwargs)

    def warning(self, event=None, *args, **kwargs):
        return self.collect_and_proxy_to_logger("warning", event, *args, **kwargs)

    warn = warning

    def error(self, event=None, *args, **kwargs):
        return self.collect_and_proxy_to_logger("error", event, *args, **kwargs)

    def critical(self, event=None, *args, **kwargs):
        return self.collect_and_proxy_to_logger("critical", event, *args, **kwargs)

    fatal = critical

    def exception(self, event=None, *args, **kwargs):
        kwargs.setdefault("exc_info", True)
        return self.collect_and_proxy_to_logger("error", event, *args, **kwargs)
