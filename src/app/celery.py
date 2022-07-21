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
    "task_serializer": "json",
    "acceot_content": [
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
    "CELERY_BEAT_SCHEDULE": {
        # "your_schedule_name": {
        #     "task": "module.file.function_name",
        #     "schedule": settings.CELERY_BEAT_RUNS_EACH_N_MINUTES * MINUTE_SECONDS,
        #     "args": (),
        #     "options": {
        #         "queue": settings.DEFAULT_QUEUE_NAME,
        #         "expires": settings.CELERY_BEAT_EXPIRES_IN_N_DAYS * DAY_SECONDS,
        #     },
        # },
    },
    "task_routes": {"module.file.*": {"queue": settings.DEFAULT_QUEUE_NAME}},
    "broker_url": settings.BROKER_URL,
}  # type: ignore

app.autodiscover_tasks(packages=[])
app.conf.update(**CELERY_CONFIG)
