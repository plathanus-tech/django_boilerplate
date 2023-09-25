from typing import Protocol


class ServiceLoader(Protocol):
    def __call__(self) -> "ExternalService":
        ...


class ExternalService:
    service_loader: ServiceLoader
    suitable_for_production: bool

    def __repr__(self):
        return self.__class__.__name__


class InternalService(ExternalService):
    pass
