import os
from datetime import timedelta

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
    "beat_schedule": {
        "push_notification_confirm_delivery_of_sent_notifications_every_15_minutes": {
            "task": "push_notifications.tasks.push_notification_confirm_delivery_periodically",
            "schedule": timedelta(minutes=15),
            "args": (),
            "options": {"expires": timedelta(minutes=10).total_seconds()},
        },
    },
    "broker_url": settings.BROKER_URL,
    "broker_connection_retry_on_startup": True,
}

app.autodiscover_tasks(["push_notifications"])
app.conf.update(**CELERY_CONFIG)
