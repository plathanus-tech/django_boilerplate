import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.conf")

app = Celery("app")

CELERY_CONFIG = {
    "task_serializer": "json",
    "accept_content": [
        "json",
    ],
    "result_serializer": "json",
    "result_backend": None,
    "enable_utc": True,
    "enable_remote_control": False,
    "default_queue": settings.DEFAULT_QUEUE_NAME,
    "acks_late": settings.CELERY_ACKS_LATE,
    "track_started": settings.CELERY_TRACK_STARTED,
    "prefetch_multiplier": settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    "task_always_eager": settings.CELERY_ALWAYS_EAGER,
    "beat_schedule": {},
    "broker_url": settings.BROKER_URL,
    "broker_connection_retry_on_startup": True,
}

app.autodiscover_tasks(["users"])
app.conf.update(**CELERY_CONFIG)
