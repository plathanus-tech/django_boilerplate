from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.drf.openapi import limit_offset_openapi_schema, openapi_schema
from app.drf.viewsets import AppViewSet
from push_notifications import selectors, services

from . import schemas


class PushNotificationViewSet(AppViewSet):
    permission_classes = [IsAuthenticated]

    @limit_offset_openapi_schema(
        wrapped_schema=schemas.PushNotificationOutputSchema,
        operation_id="push-notification-list",
        summary="Notifications list",
        description="Returns a list of notifications",
        request=None,
        tags=["push notifications"],
        add_unauthorized_response=True,
        parameter_serializer=schemas.PushNotificationInputSchema,
    )
    def list(self, request: Request) -> Response:
        params = self.get_valid_query_params(srlzr_class=schemas.PushNotificationInputSchema)
        qs = selectors.push_notification_get_viewable_qs(user=request.user, filters=params)
        return self.get_paginated_response(
            queryset=qs, srlzr_class=schemas.PushNotificationOutputSchema
        )

    @openapi_schema(
        summary="Read many notifications",
        description="Reads a list of notifications",
        request=schemas.PushNotificationReadManyInputSchema,
        responses={200: schemas.PushNotificationReadManyOutputSchema},
        tags=["push notifications"],
        operation_id="push-notifications-read",
        add_bad_request_response=True,
        add_unauthorized_response=True,
    )
    @action(methods=["PATCH"], detail=False, url_path="read")
    def read_many(self, request: Request) -> Response:
        data = self.get_valid_data(srlzr_class=schemas.PushNotificationReadManyInputSchema)
        updated = services.push_notification_read_many(reader=request.user, ids=data.get("ids"))
        return Response(data={"read": updated})

    @openapi_schema(
        summary="Read notification",
        description="Reads a single notification",
        request=None,
        responses={200: schemas.PushNotificationOutputSchema},
        tags=["push notifications"],
        operation_id="push-notification-read",
        add_not_found_response=True,
        add_bad_request_response=True,
        add_unauthorized_response=True,
    )
    @action(methods=["PATCH"], detail=True)
    def read(self, request: Request, id: int) -> Response:
        notification = get_object_or_404(
            selectors.push_notification_get_viewable_qs(user=request.user),
            pk=id,
        )
        notification = services.push_notification_read(push_notification=notification)
        out_srlzr = schemas.PushNotificationOutputSchema(instance=notification)
        return Response(data=out_srlzr.data)
