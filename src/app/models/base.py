import functools
import uuid
from collections.abc import Collection
from typing import Any, Self

from django.db import models
from django.forms import ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _


class UUIDPrimaryKeyField(models.UUIDField):
    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("verbose_name", _("id"))
        kwargs.setdefault("default", uuid.uuid4)
        kwargs.setdefault("primary_key", True)
        kwargs.setdefault("editable", False)
        super().__init__(**kwargs)


# Monkey patch the ModelForm._post_clean method in order to call a custom hook
# defined on our BaseModel class.
original_post_clean = ModelForm._post_clean  # type: ignore


def post_clean_patch(form: ModelForm):
    if issubclass(form._meta.model, BaseModel):
        # only inject form_errors to the full_clean if the model can handle it
        form.instance.full_clean = functools.partial(
            form.instance.full_clean, form_errors=form.errors
        )
    original_post_clean(form)


ModelForm._post_clean = post_clean_patch  # type: ignore


class BaseModel(models.Model):
    """This is a NOT regular django-model, please refer to the `full_clean` method defined
    below, and also to the custom hook `clean_valid_data` docstrings for more informations.
    Also notice that the `ModelForm` class gets monkey-patched in order for this to work.
    You can refer to this post for more details: https://forum.djangoproject.com/t/model-clean-after-errors-on-model-full-clean/23990
    """

    id: int

    objects: models.Manager[Self]

    class Meta:
        abstract = True

    def full_clean(  # type: ignore
        self,
        exclude: Collection[str] | None = None,
        validate_unique: bool = True,
        validate_constraints: bool = True,
        form_errors=None,
    ) -> None:
        """Overrides the default-behavior of full_clean in order to call our custom-hook `clean_valid_data`
        if no errors were provided or fields were excluded, the `form_errors` parameter is injected via
        monkey-patching, see the `post_clean_patch` method above."""

        # let the normal validation occurs, if any errors happen they will be raised
        super().full_clean(exclude, validate_unique, validate_constraints)

        if form_errors:
            return
        # now apply our custom validation, if there are no errors on the injected form_errors
        errors: dict[str, Any] = {}
        try:
            self.clean_valid_data()
        except ValidationError as e:
            e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)

    def clean_valid_data(self) -> None:
        """Custom hook that may be implemented on subclasses.

        This is mainly useful if you want to validate a model instance after all
        validations have been done, including modelforms, the default behavior of
        the `clean` is to get called even with bad data so the `clean` method is not
        a good candidate for checks that may expect only valid data (that will correspond
        exactly to your fields definitions, if a field has `null=True` then you should expect
        that the value may be `None` but for a non-null field you can expect the exact type)"""
        pass


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
