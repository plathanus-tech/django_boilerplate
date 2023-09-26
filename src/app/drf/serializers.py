from rest_framework import serializers


def inline_serializer(
    *,
    name: str,
    fields: dict[str, serializers.Field],
    data=None,
    **kwargs,
) -> serializers.Serializer:
    Serializer = type(name, (serializers.Serializer,), fields)

    if data is not None:
        return Serializer(data=data, **kwargs)

    return Serializer(**kwargs)
