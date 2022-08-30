from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.base.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra):
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra):
        user = self.create_user(email, password=password, **extra)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = None  # Removes username field
    email = models.EmailField(_("Email address"), unique=True)
    full_name = models.CharField(_("Full name"), max_length=255)

    # Permissions
    is_active = models.BooleanField(_("Is active"), default=True)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_superuser = models.BooleanField(_("Is admin"), default=False)

    # Meta
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "full_name",
    ]

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.full_name.split(" ")[0]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Group(DjangoGroup):
    """Defining this here allow to group the django model `Group`
    together in this users app."""

    class Meta:
        proxy = True
        verbose_name = _("User Group")
        verbose_name_plural = _("User Groups")
