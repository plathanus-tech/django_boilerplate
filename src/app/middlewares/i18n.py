from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils import timezone, translation

from .base import BaseMiddleware


class TimezoneMiddleware(BaseMiddleware):
    """Sets the timezone for the current request"""

    def __call__(self, request: HttpRequest) -> HttpResponse:
        tzname = settings.TIME_ZONE
        if request.user.is_authenticated:
            tzname = request.user.time_zone
        timezone.activate(tzname)
        response = self.get_response(request)
        response.headers.setdefault("x-tz-name", tzname)
        response.headers.setdefault("x-tz-utc-offset", timezone.localtime().strftime("%z"))
        return response


class LanguageMiddleware:
    """Sets the language of the translation for the current request"""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        language_code = settings.LANGUAGE_CODE
        if request.user.is_authenticated:
            language_code = request.user.language_code
        translation.activate(language_code)
        response = self.get_response(request)
        response.headers.setdefault("Content-Language", language_code)
        return response
