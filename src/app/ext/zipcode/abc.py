from typing import TypedDict

from django.conf import settings

from app.ext.abc import ExternalService


class ZipCodeData(TypedDict):
    line: str
    district: str
    city: str
    federal_unity: str
    zip_code: str


def zipcode_external_service_loader() -> "ZipcodeExternalService":
    from .backends.correios import CorreiosZipcodeExternalService
    from .backends.static import StaticZipcodeExternalService

    services = {
        "correios": CorreiosZipcodeExternalService,
        "dev.static": StaticZipcodeExternalService,
    }
    backend = settings.ZIPCODE_EXTERNAL_SERVICE_BACKEND
    return services[backend]()


class ZipcodeExternalService(ExternalService):
    service_loader = zipcode_external_service_loader

    def query(self, zip_code: str) -> list[ZipCodeData]:
        raise NotImplementedError("Missing implementation for method")
