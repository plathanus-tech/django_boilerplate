from typing import Protocol


class DecoratedTaskFunction(Protocol):
    """A task that it's created at runtime by celery."""

    def __call__(self, *args, **kwargs):
        ...

    def delay(self, *args, **kwargs):
        ...


def task(bind: bool = False):
    """A wrapper around celery.shared_task decorator.
    This decorator does nothing at runtime. It only serves static typing purposes."""

    def wrapped(fn) -> DecoratedTaskFunction:
        from celery import shared_task

        return shared_task(bind=bind)(fn)  # type: ignore

    return wrapped
