from django.urls import path

from . import views

urlpatterns = [
    path(
        "auth/",
        views.auth,
        name="auth",
    ),
    path("refresh/", views.refresh, name="refresh"),
    path("me/", views.delete, name="delete"),
]
