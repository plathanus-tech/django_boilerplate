import logging


class HealthCheckFilter:
    def filter(self, record: logging.LogRecord):
        msg = record.getMessage()
        should_display = "/health-check" not in msg and "Broken pipe from" not in msg
        return should_display
