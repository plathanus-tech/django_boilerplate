from dataclasses import dataclass
from typing import Literal

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import serializers as jwt_schemas

from app.consts.http import HttpStatusCode
from app.drf.openapi import openapi_schema
from app.drf.viewsets import AppViewSet
from users.services import auth

from . import schemas


@dataclass
class TokenDTO:
    type: Literal["Token", "Bearer"]
    access: str
    refresh: str | None = None


class AuthenticationViewSet(AppViewSet):
    permission_classes = [AllowAny]

    @openapi_schema(
        summary="Token authentication",
        description="Authenticates and returns a static Token that can be "
        "used to access protected endpoints",
        request=schemas.AuthenticationInputSchema,
        responses={HttpStatusCode.HTTP_200_OK: schemas.TokenAuthenticationOutputSchema},
        tags=["auth"],
        operation_id="authentication:token",
        add_bad_request_response=True,
        add_unauthorized_response=True,
        raises=[auth.InactiveOrInexistentAccount, auth.InvalidCredentials],
    )
    @action(methods=["POST"], detail=False, url_path="token")
    def token(self, request: Request):
        data = self.get_valid_data(srlzr_class=schemas.AuthenticationInputSchema)
        user, token = auth.token_authenticate(**data)
        user.token = TokenDTO(type="Token", access=token.key, refresh=None)  # type: ignore
        srlzr = schemas.TokenAuthenticationOutputSchema(instance=user)
        return Response(data=srlzr.data, status=200)

    @openapi_schema(
        summary="JWT authentication",
        description="Authenticates and returns a JWT Token that can be "
        "used to access protected endpoints",
        request=schemas.AuthenticationInputSchema,
        responses={HttpStatusCode.HTTP_200_OK: schemas.JwtTokenAuthenticationOutputSchema},
        tags=["auth"],
        operation_id="authentication:jwt-token",
        add_bad_request_response=True,
        add_unauthorized_response=True,
        raises=[auth.InactiveOrInexistentAccount, auth.InvalidCredentials],
    )
    @action(methods=["POST"], detail=False, url_path="jwt")
    def jwt_token(self, request: Request):
        data = self.get_valid_data(srlzr_class=schemas.AuthenticationInputSchema)
        user = auth.authenticate(**data)

        refresh = jwt_schemas.TokenObtainPairSerializer().get_token(user)
        token = TokenDTO(type="Bearer", access=str(refresh.access_token), refresh=str(refresh))
        user.token = token  # type: ignore
        srlzr = schemas.JwtTokenAuthenticationOutputSchema(instance=user)
        return Response(data=srlzr.data, status=200)

    @openapi_schema(
        summary="JWT Refresh",
        description="Refreshes the given access token",
        request=jwt_schemas.TokenRefreshSerializer,
        responses={HttpStatusCode.HTTP_200_OK: jwt_schemas.TokenRefreshSerializer},
        tags=["auth"],
        operation_id="authentication:jwt-refresh",
        add_bad_request_response=True,
    )
    @action(methods=["POST"], detail=False, url_path="jwt/refresh")
    def jwt_refresh(self, request: Request):
        return Response(
            data=self.get_valid_data(srlzr_class=jwt_schemas.TokenRefreshSerializer),
            status=200,
        )
