from django.contrib.auth import decorators as auth_decorators
from django.urls import include, path
from drf_spectacular import views as drf_views

from . import v1

schema_view = drf_views.SpectacularAPIView.as_view()
swagger_view = drf_views.SpectacularSwaggerView.as_view(url_name="schema")
redoc_view = drf_views.SpectacularRedocView.as_view(url_name="schema")

app_name = "api"
urlpatterns = [
    path("v1/", include((v1.urls, "api"), namespace="v1")),
    path("schema/", auth_decorators.login_required(schema_view), name="schema"),
    path("docs/", auth_decorators.login_required(swagger_view), name="docs"),
    path("redoc/", auth_decorators.login_required(redoc_view), name="redoc"),
]
