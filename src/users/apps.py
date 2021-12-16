from django.apps import AppConfig
from rest_framework.authtoken.apps import AuthTokenConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"


AuthTokenConfig.icon_name = "code"
