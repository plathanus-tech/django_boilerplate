from django.conf import settings
from django.contrib import admin
from django.contrib.auth import decorators as auth_decorators
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import include, path, reverse
from drf_spectacular import views as drf_views

schema_view = drf_views.SpectacularAPIView.as_view()
swagger_view = drf_views.SpectacularSwaggerView.as_view(url_name="schema")
redoc_view = drf_views.SpectacularRedocView.as_view(url_name="schema")


urlpatterns = [
    path("health-check", lambda r: HttpResponse("Ok")),
    path("", lambda r: redirect(reverse("admin:login"))),
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
    path("api/schema/", auth_decorators.login_required(schema_view), name="schema"),
    path("api/docs/", auth_decorators.login_required(swagger_view), name="docs"),
    path("api/redoc/", auth_decorators.login_required(redoc_view), name="redoc"),
    path("api/", include("api.urls", namespace="api")),
]
