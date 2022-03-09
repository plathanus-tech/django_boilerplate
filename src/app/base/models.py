import os
import random
import string
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


def generate_random_id_for_test():
    return "".join(random.choices(string.hexdigits, k=32))


def get_id_field():

    if "test" in os.environ["DJANGO_SETTINGS_MODULE"]:
        return models.CharField(
            primary_key=True, max_length=32, default=generate_random_id_for_test
        )
    return models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)


class BaseModel(models.Model):

    id = get_id_field()

    class Meta:
        abstract = True


class AutoTimeStampModel(BaseModel):

    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, blank=True, editable=False
    )
    last_updated_at = models.DateTimeField(
        verbose_name=_("updated at"), auto_now=True, blank=True, editable=False
    )

    class Meta:
        abstract = True
        get_latest_by = "last_updated_at"
        indexes = [
            models.Index(fields=["-last_updated_at"]),
        ]
