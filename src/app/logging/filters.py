import logging

from django.conf import settings


class StaticFilesFilter:
    """Filters /static/ requests records, keeping them only if it fails."""

    def filter(self, record: logging.LogRecord):
        if "/static/" not in record.getMessage():
            return True
        return record.levelno >= logging.WARNING


class AdminRoutesFilter:
    """Filters **admin/ requests records keeping them only if it fails."""

    def filter(self, record: logging.LogRecord):
        return (
            f"/{settings.ADMIN_URL_PREFIX}/" not in record.getMessage()
            or record.levelno >= logging.WARNING
        )
