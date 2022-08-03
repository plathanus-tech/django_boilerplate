import logging


class StaticFilesFilter:
    """Filters /static/ requests records, keeping them only if it fails."""

    def filter(self, record: logging.LogRecord):
        if "/static/" not in record.getMessage():
            return True
        return record.levelno >= logging.WARNING
