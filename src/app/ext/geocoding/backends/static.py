from app.ext.geocoding.abc import (
    ForwardedGeoLocation,
    GeocodingExternalService,
    GeocodingServiceUnavailable,
)


class StaticGeocodingExternalService(GeocodingExternalService):
    suitable_for_production = False

    def __init__(self, fail=False):
        self.fail = fail

    def lat_long_from_address(self, address: str) -> ForwardedGeoLocation | None:
        if self.fail:
            raise GeocodingServiceUnavailable()
        return {"latitude": -27.506877, "longitude": -48.632154}
