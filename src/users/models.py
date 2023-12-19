from typing import Any, Iterable

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.models import PermissionsMixin as DjangoPermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from app.consts.i18n import Language, TimeZoneName
from app.exceptions import InsufficientPermissions
from app.logging.utils import get_logger
from app.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra):
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)  # type: ignore
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra):
        user = self.create_user(email, password=password, **extra)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


LOGGER = get_logger("users.perms")


class PermissionsMixin(DjangoPermissionsMixin):
    """Subclass of the django PermissionsMixin class.
    Django built-in permission system does not check for object-level permissions,
    when `has_perm` is called with an `obj` it will return a `False` (because it's not implemented).
    So this mixin adds object-level permission by checking if the user has permission to perform some action
    on the object. Keep in mind that object-level permissions checks are only done if the user has permission
    to perform the action (if a user does not have the `change` permission for some model, the object-level
    permission of that model won't be checked).

    In order to check for object-level permissions there's two main ways of doing it, all of these methods
    should be written in the target class. For example, to check if a `User` have permission to perform some action
    on the `PushNotification` model, you can:

    Define a 'generic' permission check:
    ```python
    class PushNotification(BaseModel):
        # some fields here
        def has_obj_perm(self, action: str, user: User) -> bool:
            # Do something here with the `user` and the push notification (`self`)
            # `action` is the permission name, for example: the defaults would be one of:
            # `add`, `change`, `delete`, `view`
            ...
    ```

    Define a 'specific' permission check:
    ```python
    class PushNotification(BaseModel):
        # some fields here
        def has_add_obj_perm(self, user: User) -> bool:
            # Do something here with the `user` and the push notification (`self`)
            ...
    ```
    Notice that the method name is called `has_<action>_obj_perm` and differently from the generic
    check it not receives the `action`, because that's already defined on the method name.
    Also, be aware that specific checks have precedence over generic checks, so if you are checking for the
    `add` permission and you have a method called `has_add_obj_perm` and a `has_obj_perm` method that also checks
    for the `add` action, only the `has_add_obj_perm` method will be called.

    Keep in mind that these methods can be called several times, specially on the admin interface,
    so you would likely want to cache the results of a expensive calculation / thirdy party request.
    For example, if your check would require looking up the database, would be better to do only one query
    by reusing a queryset, saving in a variable the object returned by the queryset, using the related descriptors.

    These checks are triggered by the `user.has_perm` call, that is the built-in way to check. So if a
    object is passed on the `user.has_perm` call then the object-level checks are triggered, otherwise not.

    Inactive users won't have permissions and superusers will always have permissions (this is the default behavior
    from the django permissions system), in these situations the object-level check methods won't be called.
    """

    is_staff = models.BooleanField(
        _("is staff"),
        help_text=_("Only staff users can access the admin"),
        default=False,
    )
    is_superuser = models.BooleanField(
        _("is admin"),
        help_text=_("Super users have all permissions"),
        default=False,
    )

    def has_perm(self, perm: str, obj: Any | None = None) -> bool:
        if not self.is_active:  # type: ignore
            return False
        if self.is_superuser:
            return True

        if obj is None:
            return super().has_perm(perm, obj=None)
        return super().has_perm(perm, obj=None) and self.has_object_perm(perm, obj)

    def has_object_perm(self, perm: str, obj: models.Model) -> bool:
        app_name, codename = perm.split(".")
        action, modelname = codename.split("_")
        logger = LOGGER.bind(perm=perm, obj=obj, app_name=app_name, model_name=modelname)

        specific_check_func = getattr(obj, "has_%s_obj_perm" % action, None)
        if specific_check_func is not None:
            logger.debug("Calling specific obj permission check")
            return specific_check_func(user=self)
        generic_check_func = getattr(obj, "has_obj_perm", None)
        if generic_check_func is not None:
            logger.debug("Calling generic obj permission check")
            return generic_check_func(action=action, user=self)

        logger.debug("Object-level check not performed")
        return True

    def require_perm(
        self,
        perm: str,
        obj: Any | None = None,
        error_class: type[InsufficientPermissions] = InsufficientPermissions,
        **error_init_kwargs,
    ) -> None:
        if not self.has_perm(perm, obj=obj):
            raise error_class(**error_init_kwargs)

    def require_perms(
        self,
        perms: Iterable[str],
        obj: Any | None = None,
        error_class: type[InsufficientPermissions] = InsufficientPermissions,
        **error_init_kwargs,
    ) -> None:
        if not all(self.has_perm(perm, obj=obj) for perm in perms):
            raise error_class(**error_init_kwargs)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = None  # Removes username field
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=255)
    notification_token = models.CharField(
        verbose_name=_("notification token"),
        help_text=_("The token used to send push notifications to the user's phone"),
        max_length=128,
        null=True,
        blank=True,
    )
    language_code = models.CharField(
        verbose_name=_("preference language"),
        default=Language.PT_BR,
        choices=Language.choices,
        max_length=8,
    )
    time_zone = models.CharField(
        verbose_name=_("preference time zone"),
        default=TimeZoneName.AMERICA_SAO_PAULO,
        choices=TimeZoneName.choices,
        max_length=32,
    )
    is_active = models.BooleanField(
        _("is active"),
        help_text=_("Inactive users can't login. Use this instead of deleting the user."),
        default=True,
    )
    # Meta
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "full_name",
    ]

    # FK Typing
    auth_token: Token

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.full_name.split(" ")[0]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Group(DjangoGroup):
    """Defining this here allow to group the django model `Group`
    together in this users app."""

    class Meta:
        proxy = True
        verbose_name = _("user group")
        verbose_name_plural = _("user groups")
