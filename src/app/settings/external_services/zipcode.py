from app.settings.env import env

ZIPCODE_EXTERNAL_SERVICE_BACKEND = env("ZIPCODE_EXTERNAL_SERVICE_BACKEND", default="dev.static")
