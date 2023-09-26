from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .serializers import inline_serializer


class ContextGetterDefault:
    """
    A default that returns a default based on a context variable passed over to it's parent serializers.
    https://www.django-rest-framework.org/api-guide/fields/#default
    """

    requires_context = True

    def __init__(self, context_key: str):
        self.context_key = context_key

    def __call__(self, serializer_field):
        return serializer_field.context[self.context_key]


def create_choice_human_field(name: str, choices, **kwargs) -> type[serializers.ChoiceField]:
    """Function that wraps the creation of a choice field.
    This is a function and not a class directly in order to
    define the choices inside the `extend_schema_field`
    this will populate the documentation correctly"""

    class BaseHumanField(serializers.ChoiceField):
        def __init__(self, **kwargs):
            super().__init__(choices, **kwargs)

        def to_representation(self, value):
            if value in ("", None):
                return None
            return {"value": value, "human": self._choices.get(value, None)}

    field_name = "{}ChoiceHumanField".format(name.title())
    _ChoiceHumanField = type(field_name, (BaseHumanField,), {})
    return extend_schema_field(
        inline_serializer(
            name=field_name,
            fields={
                "value": serializers.ChoiceField(choices=choices),
                "human": serializers.CharField(),
            },
            required=False,
            allow_null=True,
        )
    )(_ChoiceHumanField)
