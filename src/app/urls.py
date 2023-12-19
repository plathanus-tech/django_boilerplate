from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import include, path, reverse

urlpatterns = [
    path("health-check", lambda r: HttpResponse("Ok")),
    path("", lambda r: redirect(reverse("admin:login"))),
    path("jet/", include("jet.urls", "jet")),
    path(f"{settings.ADMIN_URL_PREFIX}/", admin.site.urls),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/", include("api.urls", namespace="api")),
]
