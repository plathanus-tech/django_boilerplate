from typing import TypedDict

from django.conf import settings

from app.ext.abc import ExternalService


class ForwardedGeoLocation(TypedDict):
    latitude: float
    longitude: float


class GeocodingServiceUnavailable(Exception):
    pass


def geocoding_external_service_loader():
    from .backends.google import GoogleMapsGeocodingExternalService
    from .backends.position_stack import PositionStackGeocodingExternalService
    from .backends.static import StaticGeocodingExternalService

    services = {
        "dev.static": StaticGeocodingExternalService,
        "position_stack": PositionStackGeocodingExternalService,
        "google": GoogleMapsGeocodingExternalService,
    }
    backend = settings.GEOLOCATION_EXTERNAL_SERVICE_BACKEND
    return services[backend]()


class GeocodingExternalService(ExternalService):
    service_loader = geocoding_external_service_loader

    def lat_long_from_address(self, address: str) -> ForwardedGeoLocation | None:
        raise NotImplementedError("Missing implementation for method get_latitude_longitude")
