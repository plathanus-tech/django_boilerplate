from .urls import urlpatterns

from django.conf import settings
from django.urls import path, include


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
