from django.apps import AppConfig


class RootAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self) -> None:
        # Load openapi extensions
        from app.drf import extensions
