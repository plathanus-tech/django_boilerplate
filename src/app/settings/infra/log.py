import logging

from environ import Env

env = Env()


class HealthCheckFilter:
    def filter(self, record: logging.LogRecord):
        msg = record.getMessage()
        should_display = "/health-check" not in msg and "Broken pipe from" not in msg
        return should_display


LOGGING_LEVEL: str = env("DJANGO_LOGGING_LEVEL", default="INFO")
SENDGRID_LOGGING_LEVEL: str = env("SENDGRID_LOGGING_LEVEL", default="WARNING")
TWILIO_LOGGING_LEVEL: str = env("TWILIO_LOGGING_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {module} {asctime}: {message}",
            "style": "{",
        },
    },
    "filters": {
        "health_check_filter": {"()": "app.settings.infra.log.HealthCheckFilter"},
    },
    "root": {"handlers": ["console"], "level": LOGGING_LEVEL},
    "loggers": {
        "django.server": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
            "filters": ["health_check_filter"],
        },
        "send_grid": {
            "handlers": ["console"],
            "level": SENDGRID_LOGGING_LEVEL,
        },
        "twilio": {
            "handlers": ["console"],
            "level": TWILIO_LOGGING_LEVEL,
        },
        "users.tasks": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
