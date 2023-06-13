from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import request, response, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from . import serializers


@extend_schema(
    request=serializers.LoginSerializer,
    responses={200: serializers.LoginTokenSerializer},
    operation_id="get-token",
    tags=["auth"],
)
@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def auth(request: request.Request) -> response.Response:
    login_srlzr = serializers.LoginSerializer(data=request.data)
    login_srlzr.is_valid(raise_exception=True)
    user = login_srlzr.user

    refresh = RefreshToken.for_user(user=user)
    logged_in_srlzr = serializers.LoggedUserSerializer(instance=user)
    out_data = {
        "user": logged_in_srlzr.data,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "token_type": "Bearer",
    }
    srlzr_login = serializers.LoginTokenSerializer(out_data)
    return response.Response(data=srlzr_login.data, status=status.HTTP_200_OK)


@extend_schema(
    request=TokenRefreshSerializer,
    responses={200: TokenRefreshSerializer},
    operation_id="token-refresh",
    tags=["auth"],
)
@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def refresh(request: request.Request) -> response.Response:
    srlzr = TokenRefreshSerializer(data=request.data)
    srlzr.is_valid(raise_exception=True)

    return response.Response(data=srlzr.validated_data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id="self-delete",
    tags=["auth"],
    responses=None,
)
@api_view(["DELETE"])
def delete(request: request.Request) -> response.Response:
    user: User = request.user
    user.is_active = False
    user.save()

    return response.Response(status=status.HTTP_204_NO_CONTENT)
