from app.settings.env import env

PUSH_NOTIFICATION_EXTERNAL_SERVICE_BACKEND = env(
    "PUSH_NOTIFICATION_EXTERNAL_SERVICE_BACKEND",
    default="dev.static",
)
