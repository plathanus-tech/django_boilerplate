from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import pytest

from app.celery.decorators import BaseTask


@pytest.fixture
def task():
    from celery.utils.threads import LocalStack

    @dataclass
    class Request:
        expires: str | None
        properties: dict[str, str]

    task = BaseTask()
    task.request_stack = LocalStack()
    task.request_stack.push(Request(expires=None, properties={}))
    return task


def test_base_task_scheduled_at_raises_when_called_without_expires(task, settings):
    assert task.request.expires is None
    settings.IS_TESTING = False

    with pytest.raises(ValueError):
        task.scheduled_at


def test_base_task_scheduled_at_returns_now_when_called_without_expires_with_is_testing(
    task, settings
):
    assert task.request.expires is None
    settings.IS_TESTING = True

    dt = task.scheduled_at
    assert isinstance(dt, datetime)


def test_base_task_scheduled_at_returns_correct_scheduled_at(task):
    now = datetime(2023, 9, 26, 17, 0, 0, tzinfo=timezone(timedelta(0), "UTC"))
    expires = now + timedelta(seconds=30)

    task.request.expires = expires.isoformat()
    task.request.properties["expiration"] = "30000"

    scheduled_at = task.scheduled_at
    assert scheduled_at == now
