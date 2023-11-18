from django.urls import include, path

from . import auth, push_notifications, users

urlpatterns = [
    path("auth/", include((auth.urls, "auth"), namespace="auth")),
    path(
        "notifications/",
        include((push_notifications.urls, "push_notifications"), namespace="push_notifications"),
    ),
    path("users/", include((users.urls, "users"), namespace="users")),
]
