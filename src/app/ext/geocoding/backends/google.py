import logging
from typing import Literal, Protocol, TypedDict, cast

import requests
from django.conf import settings

from app.ext.geocoding.abc import (
    ForwardedGeoLocation,
    GeocodingExternalService,
    GeocodingServiceUnavailable,
)


class _GoogleMapsGeocodingResultGeometryLocation(TypedDict):
    lat: float
    lng: float


class _GoogleMapsGeocodingResultGeometry(TypedDict):
    location: _GoogleMapsGeocodingResultGeometryLocation


class _GoogleMapsGeocodingResult(TypedDict):
    geometry: _GoogleMapsGeocodingResultGeometry


class _GoogleMapsGeocodingResponse(TypedDict):
    status: Literal[
        "OK",
        "ZERO_RESULTS",
        "OVER_DAILY_LIMIT",
        "OVER_QUERY_LIMIT",
        "REQUEST_DENIED",
        "INVALID_REQUEST",
        "UNKNOWN_ERROR",
    ]
    results: list[_GoogleMapsGeocodingResult]


class _GeocodingAPIClient(Protocol):
    def forward_address(self, address: str) -> _GoogleMapsGeocodingResponse:
        ...


class _GoogleMapsGeoCodingApiClient:
    def __init__(self):
        self.api_key = settings.GEOLOCATION_EXTERNAL_SERVICE_GOOGLE_MAPS_API_KEY

    def forward_address(self, address: str) -> _GoogleMapsGeocodingResponse:
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={
                "key": self.api_key,
                "address": address,
            },
            timeout=10,
        )
        return cast(_GoogleMapsGeocodingResponse, response.json())


logger = logging.getLogger(__name__)


class GoogleMapsGeocodingExternalService(GeocodingExternalService):
    suitable_for_production = True

    def __init__(self, client: _GeocodingAPIClient | None = None):
        self.client = client or _GoogleMapsGeoCodingApiClient()

    def lat_long_from_address(self, address: str) -> ForwardedGeoLocation | None:
        logger.debug("Starting google geocoding service request")
        response = self.client.forward_address(address)
        logger.info("Google service request finished")
        logger.debug(f"Received response from google geocoding service {response}")

        if response["status"] != "OK":
            logger.warning(f"Failed to fetch geolocation, {response=}")
            return None
        result = response["results"][0]
        location = result["geometry"]["location"]
        return {"latitude": location["lat"], "longitude": location["lng"]}
