from app.settings.env import env

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "app.drf.authentication.LastLoginAwareJwtAuthentication",
        "app.drf.authentication.LastLoginAwareTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "EXCEPTION_HANDLER": "app.drf.exc_handler.custom_exception_handler",
}
API_PAGINATION_DEFAULT_LIMIT = env.int("API_PAGINATION_DEFAULT_LIMIT", 50)
API_PAGINATION_MAX_LIMIT = env.int("API_PAGINATION_MAX_LIMIT", 100)
