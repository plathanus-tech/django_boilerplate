from datetime import datetime
from typing import Any, Dict, Protocol, Tuple, Union

from celery import Task
from celery.canvas import Signature


class DecoratedTaskFunction(Protocol):
    """A task that it's created at runtime by celery."""

    def __call__(self, *args, **kwargs):
        ...

    def delay(self, *args, **kwargs):
        """Shortcut to `apply_async`. No options can be given"""
        ...

    def s(self, *args, **kwargs) -> Signature:
        """Signature for Canvas calling. From [celery docs](https://docs.celeryq.dev/en/stable/getting-started/next-steps.html#designing-workflows)."""
        ...

    def apply_async(
        self,
        args: Tuple[Any, ...] = ...,
        kwargs: Dict[str, Any] = ...,
        *,
        queue: str = ...,
        countdown: float = ...,
        eta: datetime = ...,
        expires: Union[float, datetime] = ...,
        **options
    ):
        """Runs a task on the background.
        Parameters, directly from [celery docs](https://docs.celeryq.dev/en/stable/reference/celery.app.task.html?highlight=apply_async#celery.app.task.Task.apply_async).
        """
        ...


def task(
    bind: bool = False,
    *,
    autoretry_for: Tuple[Exception, ...] = None,  # type: ignore
    max_retries: int = 3,
    retry_backoff: bool = None,  # type: ignore
    rate_limit: str = None,  # type: ignore
    time_limit: int = None,  # type: ignore
    soft_time_limit: int = None,  # type: ignore
    throws: Tuple[Exception, ...] = None,  # type: ignore
    base: Task = None,
    **options
):
    """A wrapper around celery.shared_task decorator.
    This decorator does nothing at runtime. It only serves static typing purposes.
    Directly from [celery docs](https://docs.celeryq.dev/en/stable/userguide/tasks.html#task-options)."""

    def wrapped(fn) -> DecoratedTaskFunction:
        from celery import shared_task

        return shared_task(  # type: ignore
            bind=bind,
            autoretry_for=autoretry_for,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            rate_limit=rate_limit,
            time_limit=time_limit,
            soft_time_limit=soft_time_limit,
            throws=throws,
            base=base,
            **options,
        )(fn)

    return wrapped
