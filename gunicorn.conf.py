logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "health_check_filter": {"()": "app.settings.infra.log.HealthCheckFilter"},
    },
    "loggers": {
        "gunicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "filters": ["health_check_filter"],
        },
    },
}
