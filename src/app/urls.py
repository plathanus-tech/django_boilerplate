from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, reverse
from django.shortcuts import redirect
from drf_spectacular import views as drf_views

from app.base.jwt_auth import auth_token_view, refresh_view


schema_view = drf_views.SpectacularAPIView.as_view()
swagger_view = drf_views.SpectacularSwaggerView.as_view(url_name="schema")
redoc_view = drf_views.SpectacularRedocView.as_view(url_name="schema")

urlpatterns = i18n_patterns(
    path("", lambda r: redirect(reverse("admin:login"))),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("", include("rest_framework.urls", namespace="rest_framework")),
    path("api/schema/", schema_view, name="schema"),
    path("api/docs/", swagger_view, name="docs"),
    path("api/redoc/", redoc_view, name="redoc"),
    path("api/auth/", auth_token_view, name="token_obtain_pair"),
    path("api/auth/refresh/", refresh_view, name="token_refresh"),
    prefix_default_language=True,
)

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
