import logging
from typing import Any, TypedDict

import requests
from django.conf import settings

from app.ext.geocoding.abc import (
    ForwardedGeoLocation,
    GeocodingExternalService,
    GeocodingServiceUnavailable,
)


class _PositionStackResponseDataSchema(TypedDict):
    latitude: float
    longitude: float


class _PositionStackResponseSchema(TypedDict):
    data: list[_PositionStackResponseDataSchema]


logger = logging.getLogger(__name__)


class PositionStackGeocodingExternalService(GeocodingExternalService):
    # Altough this service is suitable for production, it's not precise!
    suitable_for_production = True

    def __init__(self):
        self.s = requests.Session()
        self.access_keys: list[
            str
        ] = settings.GEOLOCATION_EXTERNAL_SERVICE_POSITION_STACK_ACCESS_KEYS

    def lat_long_from_address(self, address: str) -> ForwardedGeoLocation | None:
        logger.info("Starting position stack forward geo coding service request")

        params: dict[str, Any] = {"country": "BR", "limit": 1, "query": address}
        for access_key in self.access_keys:
            params["access_key"] = access_key
            # We must use HTTP because the free plan does not cover HTTPS
            response = self.s.get("http://api.positionstack.com/v1/forward", params=params)
            if not response.ok:
                logger.warning(f"Failed to fetch data {response.text=} moving to next access_key")
                continue
            response_data: _PositionStackResponseSchema = response.json()
            data = response_data["data"]
            if data and isinstance(data[0], dict):
                logger.info(f"Found data for query address {data=}")
                return data[0]
            logger.warning("No data found for query address")
            return None
        logger.critical(f"Failed to forward geo location, all access_keys failed")
        raise GeocodingServiceUnavailable("All access keys used, no one seems to be working")
