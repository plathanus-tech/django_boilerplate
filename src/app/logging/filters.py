import logging


class HealthCheckFilter:
    def filter(self, record: logging.LogRecord):
        return "/health-check" not in record.getMessage() or record.levelno >= logging.WARNING
