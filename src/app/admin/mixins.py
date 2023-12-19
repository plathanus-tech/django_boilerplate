from typing import Literal

from django.contrib.auth import get_permission_codename
from django.http.request import HttpRequest

from app.models.base import BaseModel


def no_permission(*args, **kwargs) -> bool:
    """A callable that will always return False"""
    return False


class ReadOnlyAdminMixin:
    """A read-only admin. It must be inherited before the `admin.ModelAdmin` due to python's MRO."""

    has_add_permission = no_permission
    has_delete_permission = no_permission
    has_change_permission = no_permission


class ObjectPermissionMixin:
    """Mixin that handles object-level permissions, It must be inherited before the `admin.ModelAdmin`.
    The default implementation of the `has_change_permission` and `has_delete_permission`
    does not passes the `obj` received to the `user.has_perm` check because by default the
    django built-in permission system will return `False` when an object is passed along.
    So we override the methods that receive the object (change/delete) so they pass the
    object to the `user.has_perm`, because our user model has overriden it as well.
    For more information check the docstring on the `users.models.PermissionMixin` class"""

    def has_change_permission(self, request: HttpRequest, obj: BaseModel | None = None) -> bool:
        return self.has_object_permission(request, obj, action="change")

    def has_delete_permission(self, request: HttpRequest, obj: BaseModel | None = None) -> bool:
        return self.has_object_permission(request, obj, action="delete")

    def has_object_permission(
        self, request: HttpRequest, obj: BaseModel | None, action: Literal["change", "delete"]
    ):
        opts = self.opts  # type: ignore
        codename = get_permission_codename(action, opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename), obj)
