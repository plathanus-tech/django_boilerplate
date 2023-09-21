from environ import Env

from .redis import REDIS_URL

env = Env()


DEFAULT_QUEUE_NAME: str = env("DEFAULT_QUEUE_NAME", default="default")
CELERY_ACKS_LATE: bool = env("CELERY_ACKS_LATE", default=True)
CELERY_TRACK_STARTED: bool = env("CELERY_TRACK_STARTED", default=False)
CELERY_WORKER_PREFETCH_MULTIPLIER: int = env("CELERY_WORKER_PREFETCH_MULTIPLIER", default=1)
CELERY_BEAT_EXPIRES_IN_N_DAYS: int = env("CELERY_BEAT_EXPIRES_IN_N_DAYS", default=3)
CELERY_ALWAYS_EAGER: bool = env("CELERY_ALWAYS_EAGER", default=False)
BROKER_URL = REDIS_URL
