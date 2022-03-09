from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.apps import AuthTokenConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = _("User")
    verbose_name_plural = _("Users")
    icon_name = "assignment_ind"


AuthTokenConfig.icon_name = "code"
