from typing import Any

from rest_framework import request, serializers


def get_valid_request_query_params(
    *, request: request.Request, srlzr_class: type[serializers.Serializer]
) -> dict[str, Any]:
    srlzr = srlzr_class(data=request.query_params)
    srlzr.is_valid(raise_exception=True)
    return srlzr.validated_data


def get_valid_request_data(
    *, request: request.Request, srlzr_class: type[serializers.Serializer]
) -> dict[str, Any]:
    srlzr = srlzr_class(data=request.data)
    srlzr.is_valid(raise_exception=True)
    return srlzr.validated_data
