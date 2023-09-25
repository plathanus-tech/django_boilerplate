import django_filters
from django.db.models import QuerySet

from push_notifications import models
from users.models import User


class PushNotificationFilterSet(django_filters.FilterSet):
    only_read = django_filters.BooleanFilter(
        field_name="read_at", lookup_expr="isnull", exclude=True
    )


def push_notification_get_viewable_qs(
    *, user: User, filters=None
) -> QuerySet[models.PushNotification]:
    filter_set = PushNotificationFilterSet(
        data=filters,
        queryset=models.PushNotification.objects.filter(user=user).order_by("-created_at"),
    )
    return filter_set.qs
