from typing import Protocol

from django.http import HttpRequest, HttpResponse


class _GetResponse(Protocol):
    def __call__(self, request: HttpRequest) -> HttpResponse:
        ...


class BaseMiddleware:
    def __init__(self, get_response: _GetResponse) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:
        return None
