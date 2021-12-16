from django.urls import include, path

from .api import urls

app_name = "users"
urlpatterns = [
    path("api/", include(urls)),
]
