from datetime import datetime, timedelta
from typing import Any, Dict, Protocol, Tuple, Union

from celery import Task
from celery.canvas import Signature
from django.conf import settings
from django.utils import timezone


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
        **options,
    ):
        """Runs a task on the background.
        Parameters, directly from [celery docs](https://docs.celeryq.dev/en/stable/reference/celery.app.task.html?highlight=apply_async#celery.app.task.Task.apply_async).
        """
        ...


class BaseTask(Task):
    @property
    def scheduled_at(self) -> datetime:
        """The exact time that this task was sent to the queue, this means that this task can be retried and this time will always be the same"""
        if not self.request.expires:
            if settings.IS_TESTING:
                return timezone.now()  # type: ignore
            raise ValueError(
                "Missing `expires` option, this task was not scheduled or the `expires` option was not given on BEAT_SCHEDULE"
            )
        # The amount of miliseconds this task will take to expire, with this, we can go back in time
        # per-task basis, because each task can be set with different expires times
        task_expiration = int(self.request.properties["expiration"]) / 1000
        dt = datetime.fromisoformat(self.request.expires).astimezone()
        return dt - timedelta(seconds=task_expiration)


def task(
    bind: bool = False,
    *,
    autoretry_for: Tuple[type[Exception], ...] | None = None,
    max_retries: int = 3,
    retry_backoff: bool = False,
    rate_limit: str | None = None,
    time_limit: int | None = None,
    soft_time_limit: int | None = None,
    throws: Tuple[Exception, ...] | None = None,
    base: Task = BaseTask,
    **options,
):
    """A wrapper around celery.shared_task decorator.
    This decorator does nothing at runtime. It only serves static typing purposes.
    Directly from [celery docs](https://docs.celeryq.dev/en/stable/userguide/tasks.html#task-options).
    """

    def wrapped(fn) -> DecoratedTaskFunction:
        from celery import shared_task

        return shared_task(  # type: ignore
            bind=bind,
            autoretry_for=autoretry_for or (),
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
