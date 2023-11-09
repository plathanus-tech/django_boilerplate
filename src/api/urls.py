from django.urls import include, path
from drf_spectacular import views as drf_views

from . import v1

app_name = "api"
urlpatterns = [
    path("v1/", include((v1.urls, "api"), namespace="v1")),
    path("schema/", drf_views.SpectacularAPIView.as_view(), name="schema"),
    path("docs/", drf_views.SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("redoc/", drf_views.SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
