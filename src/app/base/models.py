from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id: int

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
