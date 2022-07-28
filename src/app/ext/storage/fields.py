import os
from typing import Type

from django.core.files.storage import Storage, default_storage
from django.db.models import FileField, ImageField

from .aws_s3 import PrivateMediaStorage, PublicMediaStorage


def _is_on_prod():
    SETTINGS_MODULE = os.environ["DJANGO_SETTINGS_MODULE"]
    return "prod" in SETTINGS_MODULE


def _get_storage_class(prod_storage_class: Type[Storage]):
    if _is_on_prod():
        return prod_storage_class
    return default_storage


class PublicFileField(FileField):
    """A public file field, all users can access it."""

    def __init__(self, **kwargs):
        kwargs["storage"] = _get_storage_class(prod_storage_class=PublicMediaStorage)
        super().__init__(**kwargs)


class PrivateFileField(FileField):
    """A private file field, only logged in users can access it."""

    def __init__(self, **kwargs):
        kwargs["storage"] = _get_storage_class(prod_storage_class=PrivateMediaStorage)
        super().__init__(**kwargs)


class PublicImageField(ImageField):
    """A public image field, all users can access it."""

    def __init__(self, **kwargs):
        kwargs["storage"] = _get_storage_class(prod_storage_class=PublicMediaStorage)
        super().__init__(**kwargs)


class PrivateImageField(ImageField):
    """A public image field, only logged in users can access it."""

    def __init__(self, **kwargs):
        kwargs["storage"] = _get_storage_class(prod_storage_class=PrivateMediaStorage)
        super().__init__(**kwargs)
