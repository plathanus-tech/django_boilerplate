import json
from drf_yasg.inspectors import SwaggerAutoSchema
from . import serializers, err_messages


class AuthAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return [
            "Auth",
        ]


login = {
    "auto_schema": AuthAutoSchema,
    "operation_summary": "Login",
    "method": "POST",
    "request_body": serializers.AuthSerializer,
    "responses": {
        200: serializers.TokenSerializer,
        401: json.dumps(err_messages.INVALID_CREDENTIALS),
    },
}
