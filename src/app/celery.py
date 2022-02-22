import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.dev")

app = Celery("app")

MINUTE_SECONDS = 60
HOUR_MINUTES = 60
DAY_HOURS = 24
DAY_SECONDS = MINUTE_SECONDS * HOUR_MINUTES * DAY_HOURS

CELERY_CONFIG = {
    "CELERY_TASK_SERIALIZER": "json",
    "CELERY_ACCEPT_CONTENT": [
        "json",
    ],
    "CELERY_RESULT_SERIALIZER": "json",
    "CELERY_RESULT_BACKEND": None,
    "CELERY_ENABLE_UTC": True,
    "CELERY_ENABLE_REMOTE_CONTROL": False,
    "CELERY_DEFAULT_QUEUE": settings.DEFAULT_QUEUE_NAME,
    "CELERY_ACKS_LATE": settings.CELERY_ACKS_LATE,
    "CELERY_TRACK_STARTED": settings.CELERY_TRACK_STARTED,
    "CELERY_PREFETCH_MULTIPLIER": settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    "CELERY_BEAT_SCHEDULE": {
        "your_schedule_name": {
            "task": "module.file.function_name",
            "schedule": settings.CELERY_BEAT_RUNS_EACH_N_MINUTES * MINUTE_SECONDS,
            "args": (),
            "options": {
                "queue": settings.DEFAULT_QUEUE_NAME,
                "expires": settings.CELERY_BEAT_EXPIRES_IN_N_DAYS * DAY_SECONDS,
            },
        },
    },
    "CELERY_ROUTES": {"module.file.*": {"queue": settings.DEFAULT_QUEUE_NAME}},
    "BROKER_URL": settings.BROKER_URL,
    "BROKER_TRANSPORT": settings.BROKER_TRANSPORT,
}
