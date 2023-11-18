from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema


class LoginAwareSimpleJWTScheme(SimpleJWTScheme):
    target_class = "app.drf.authentication.LastLoginAwareJwtAuthentication"
    name = "JWT Authentication"


class LoginAwareTokenScheme(OpenApiAuthenticationExtension):
    target_class = "app.drf.authentication.LastLoginAwareTokenAuthentication"
    name = "Token Authentication"

    def get_security_definition(self, auto_schema: AutoSchema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "bearerFormat": "Token",
            "description": "Token-based authentication, requires `Token` to be prefixed",
        }
