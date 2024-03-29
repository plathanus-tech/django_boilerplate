from app.settings.env import env

GEOLOCATION_EXTERNAL_SERVICE_BACKEND = env(
    "GEOLOCATION_EXTERNAL_SERVICE_BACKEND", default="dev.static"
)

if GEOLOCATION_EXTERNAL_SERVICE_BACKEND == "google":
    GEOLOCATION_EXTERNAL_SERVICE_GOOGLE_MAPS_API_KEY = env(
        "GEOLOCATION_EXTERNAL_SERVICE_GOOGLE_MAPS_API_KEY"
    )


if GEOLOCATION_EXTERNAL_SERVICE_BACKEND == "position_stack":
    GEOLOCATION_EXTERNAL_SERVICE_POSITION_STACK_ACCESS_KEYS = env.list(
        "GEOLOCATION_EXTERNAL_SERVICE_POSITION_STACK_ACCESS_KEYS"
    )
