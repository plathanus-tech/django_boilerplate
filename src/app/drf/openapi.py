import decimal
import uuid
from typing import Sequence, Type

from django.conf import settings
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import serializers, status

from app.consts.http import HTTP_STATUS_NAME
from app.exceptions import ApplicationError


class _ApplicationErrorExtraSchema(serializers.Serializer):
    fields = serializers.DictField()


class ApplicationErrorSchema(serializers.Serializer):
    kind = serializers.CharField()
    message = serializers.CharField()
    extra = _ApplicationErrorExtraSchema()


class AuthenticationFailedSchema(serializers.Serializer):
    kind = serializers.CharField()
    message = serializers.CharField()
    extra = serializers.DictField(default={})


class InsufficientPermissionsSchema(AuthenticationFailedSchema):
    pass


def _openapi_parameters_from_serializer(
    serializer: type[serializers.Serializer],
) -> list[OpenApiParameter]:
    known_openapi_type_for_fields = {
        serializers.BooleanField: bool,
        serializers.CharField: str,
        serializers.ChoiceField: str,
        serializers.DateTimeField: str,
        serializers.DateField: str,
        serializers.DecimalField: decimal.Decimal,
        serializers.FloatField: float,
        serializers.IntegerField: int,
        serializers.UUIDField: uuid.UUID,
    }
    fields: dict[str, serializers.Field] = serializer.get_fields(serializer)
    parameters = []
    for field_name, field in fields.items():
        openapi_type = known_openapi_type_for_fields.get(type(field))
        if openapi_type is None:
            raise LookupError(
                f"Missing openapi type for {field=}, maybe you're adding a field that",
                "is not yet mapped to a openapi type, if so add the correct type entry.",
                "Remember that only query-string like fields are allowed",
            )
        choices = getattr(field, "choices", None)
        if choices is not None:
            # choices is a ordered dict on the serializer
            description = "<br>".join(
                ["`{}` - {}".format(val, label) for val, label in choices.items()]
            )
        else:
            description = field.label or ""

        default = None if field.default is serializers.empty else field.default

        parameters.append(
            OpenApiParameter(
                name=field_name,
                type=openapi_type,
                required=field.required,
                description=description,
                enum=choices,
                allow_blank=getattr(field, "blank", True),
                default=default,
            )
        )
    return parameters


def openapi_schema(
    *,
    summary: str,
    description: str,
    request: serializers.Serializer | None,
    responses: dict[int, type[serializers.Serializer] | serializers.Serializer] | None,
    tags: list[str],
    operation_id: str | None = None,
    add_bad_request_response: bool = False,
    add_unauthorized_response: bool = False,
    add_forbidden_response: bool = False,
    add_not_found_response: bool = False,
    parameter_serializer: type[serializers.Serializer] | None = None,
    raises: Sequence[type[ApplicationError]] | None = None,
    **kwargs,
):
    """Method decorator that wraper `drf_spectacular.extend_schema` with more defaults required
    and some extra behavior. If the `responses` is not `None` will include some extra responses,
    a serializer that corresponds to the custom_exception_handler they are:
    - 400: If the responses does not yet has one 400 response defined and the parameter `add_bad_request_response` is set to True;
    - 401: If the parameter `add_unathorized_response` is set to True;
    - 403: If the parameter `add_forbidden_response` is set to True;

    `parameter_serializer`: A serializer class that is used for generating the parameters directly
    from a serializer.
    """
    responses = responses or {}
    raises = raises or []

    error_response = responses.get(status.HTTP_400_BAD_REQUEST, None)
    if error_response is None and add_bad_request_response:
        responses[status.HTTP_400_BAD_REQUEST] = OpenApiResponse(
            response=ApplicationErrorSchema,
            description="Validation failed, either data or constraints",
        )
    if add_unauthorized_response:
        responses[status.HTTP_401_UNAUTHORIZED] = OpenApiResponse(
            response=AuthenticationFailedSchema,
            description="Missing credentials or credentials are invalid",
        )
    if add_forbidden_response:
        responses[status.HTTP_403_FORBIDDEN] = OpenApiResponse(
            response=InsufficientPermissionsSchema, description="Missing permissions"
        )
    if add_not_found_response:
        responses[status.HTTP_404_NOT_FOUND] = OpenApiResponse(
            response=ApplicationErrorSchema, description="Resource not found"
        )
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = OpenApiResponse(
        response=ApplicationErrorSchema, description="Unexpected failure"
    )
    responses[status.HTTP_502_BAD_GATEWAY] = OpenApiResponse(
        response=None, description="Temporary unavailability"
    )
    if parameter_serializer is not None:
        parameters = kwargs.get("parameters", [])
        parameters.extend(_openapi_parameters_from_serializer(parameter_serializer))
        kwargs["parameters"] = parameters

    if raises:
        description += "<br>*This endpoint may raise the following errors:* <br>"
    for exc in raises:
        http_code = exc.http_status_code
        if http_code not in responses:
            raise TypeError(
                f"Operation ID: {operation_id} ({summary}). "
                "A exception defined inside the `raises` clause has a status code "
                f"({http_code}) that is not documented on the `responses`"
                "Maybe you forgot to pass a `True` value to some of the `add_<error_name>_response` flags?"
            )
        description += f"<br>**{http_code} - {HTTP_STATUS_NAME[http_code]}** - `{exc.__name__}`: {exc.error_message}"

    return extend_schema(
        operation_id=operation_id,
        description=description,
        request=request,
        responses=responses,
        tags=tags,
        summary=summary,
        **kwargs,
    )


def limit_offset_openapi_schema(
    *,
    wrapped_schema: Type[serializers.Serializer],
    description: str,
    summary: str,
    tags: list[str],
    operation_id: str | None = None,
    request: serializers.Serializer | None = None,
    responses: dict[int, type[serializers.Serializer] | serializers.Serializer] | None = None,
    parameter_serializer: type[serializers.Serializer] | None = None,
    **openapi_schema_kwargs,
):
    """Wrapper around the openapi_schema decorator that also adds a responses[200] with the `wrapped_schema`
    together with the paginated schema."""
    from .serializers import inline_serializer

    schema_name = f"Paginated{wrapped_schema.__name__}"
    responses = responses or {}
    responses[200] = inline_serializer(
        name=schema_name,
        fields={
            "limit": serializers.IntegerField(),
            "offset": serializers.IntegerField(),
            "count": serializers.IntegerField(),
            "next": serializers.URLField(required=False, default=None),
            "previous": serializers.URLField(required=False, default=None),
            "results": wrapped_schema(many=True),
        },
    )
    parameters = openapi_schema_kwargs.get("parameters", [])
    parameters.extend(
        [
            OpenApiParameter(
                name="limit",
                description=f"How many results per page, max: {settings.API_PAGINATION_MAX_LIMIT}",
                type=int,
                required=False,
                default=settings.API_PAGINATION_DEFAULT_LIMIT,
            ),
            OpenApiParameter(
                name="offset",
                description="The page to lookup",
                type=int,
                required=False,
                default=0,
            ),
        ]
    )
    openapi_schema_kwargs["parameters"] = parameters
    return openapi_schema(
        operation_id=operation_id,
        description=description,
        summary=summary,
        request=request,
        responses=responses,
        tags=tags,
        parameter_serializer=parameter_serializer,
        **openapi_schema_kwargs,
    )


FILE_UPLOAD_REQUEST = {
    "multipart/form-data": {
        "type": "object",
        "properties": {"file": {"type": "string", "format": "binary"}},
    }
}
