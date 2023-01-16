import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.conf")

app = Celery("app")

MINUTE_SECONDS = 60
HOUR_MINUTES = 60
DAY_HOURS = 24
DAY_SECONDS = MINUTE_SECONDS * HOUR_MINUTES * DAY_HOURS

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
    "beat_schedule": {
        "heart_beat_each_15_minutes": {
            "task": "users.tasks.heart_beat",
            "schedule": 1 * MINUTE_SECONDS,
            "args": (),
            "options": {
                "expires": settings.CELERY_BEAT_EXPIRES_IN_N_DAYS * DAY_SECONDS,
            },
        },
    },
    "broker_url": settings.BROKER_URL,
}  # type: ignore

app.autodiscover_tasks(["users"])
app.conf.update(**CELERY_CONFIG)
