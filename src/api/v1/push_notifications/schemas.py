from rest_framework import serializers

from app.consts import push_notification as push_notification_consts
from app.drf.fields import create_choice_human_field
from app.drf.serializers import inline_serializer
from push_notifications import models


class PushNotificationInputSchema(serializers.Serializer):
    only_read = serializers.BooleanField(required=False, allow_null=True)


PushNotificationKindField = create_choice_human_field(constant_class=push_notification_consts.Kind)
PushNotificationStatusField = create_choice_human_field(
    constant_class=push_notification_consts.Status
)


class PushNotificationOutputSchema(serializers.ModelSerializer):
    kind = PushNotificationKindField()
    status = PushNotificationStatusField()
    data = inline_serializer(
        name="PushNotificationEnrichedDataOutputSchema",
        fields={
            "id": serializers.CharField(),
            "createdAt": serializers.DateTimeField(),
            "readAt": serializers.DateTimeField(),
            "timeSinceCreated": serializers.CharField(),
            "kind": serializers.CharField(),
            "meta": serializers.JSONField(),
        },
        source="enriched_data",
    )

    class Meta:
        model = models.PushNotification
        fields = (
            "id",
            "title",
            "description",
            "read_at",
            "kind",
            "status",
            "data",
        )


class PushNotificationReadManyInputSchema(serializers.Serializer):
    ids = serializers.ListField(required=False, allow_null=True)


class PushNotificationReadManyOutputSchema(serializers.Serializer):
    read = serializers.IntegerField()
