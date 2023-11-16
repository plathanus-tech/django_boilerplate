from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from app.consts.http import HttpStatusCode
from app.drf.openapi import openapi_schema
from app.drf.viewsets import AppViewSet
from users.services import account

from . import schemas


class CurrentUserViewSet(AppViewSet):
    @openapi_schema(
        summary="Current user",
        description="Returns details about the current user",
        request=None,
        responses={HttpStatusCode.HTTP_200_OK: schemas.CurrentUserOutputSchema},
        tags=["users:me"],
        operation_id="users-me",
        add_unauthorized_response=True,
    )
    def list(self, request: Request) -> Response:
        srlzr = schemas.CurrentUserOutputSchema(instance=request.user)
        return Response(srlzr.data)

    @openapi_schema(
        summary="Delete account",
        description="Deletes the account for the current user",
        request=None,
        responses={HttpStatusCode.HTTP_204_NO_CONTENT: None},
        tags=["users:me"],
        operation_id="users-me-delete-account",
        add_unauthorized_response=True,
    )
    @action(methods=["DELETE"], detail=False, url_name="delete-account", url_path="account")
    def delete_account(self, request: Request) -> Response:
        account.user_delete_account(user=request.user)
        return Response(status=204)
