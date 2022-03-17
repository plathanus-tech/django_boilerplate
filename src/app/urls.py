from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from app.base.jwt_auth import auth_token_view, refresh_view


schema_view = get_schema_view(
    openapi.Info(
        title="REST API",
        default_version="v1",
        description="Welcome to the Docs API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("rest_framework.urls", namespace="rest_framework")),
    path("docs/", schema_view.with_ui(), name="swagger"),
    path("api/auth/", auth_token_view, name="token_obtain_pair"),
    path("api/auth/refresh/", refresh_view, name="token_refresh"),
)

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
