from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone


class TimezoneMiddleware:
    """Sets the timezone for the current request"""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        full_path = request.get_full_path()
        _, locale, *_ = full_path.split("/")
        tzname = settings.TIMEZONE_FOR_LANGUAGE.get(locale, settings.TIME_ZONE)

        timezone.activate(tzname)
        return self.get_response(request)
