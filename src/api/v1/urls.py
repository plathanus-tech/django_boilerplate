from django.urls import include, path

from . import push_notifications

urlpatterns = [
    path(
        "notifications/",
        include((push_notifications.urls, "push_notifications"), namespace="push_notifications"),
    ),
]
