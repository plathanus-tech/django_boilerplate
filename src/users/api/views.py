from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from . import docs, serializers, err_messages


@csrf_exempt
@swagger_auto_schema(**docs.login)
@api_view(["POST"])
@permission_classes([AllowAny])
def auth(request: Request) -> Response:
    srlzr = serializers.AuthSerializer(data=request.data)
    srlzr.is_valid(raise_exception=True)

    data = srlzr.validated_data
    user = authenticate(email=data["email"], password=data["password"])

    if not user:
        return Response(
            data=err_messages.INVALID_CREDENTIALS,
            status=status.HTTP_401_UNAUTHORIZED,
        )
    token, _ = Token.objects.get_or_create(user=user)
    out_data = {
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
        },
        "access_token": token.key,
    }
    srlzr = serializers.TokenSerializer(out_data)
    return Response(data=srlzr.data, status=status.HTTP_200_OK)
