import functools
import inspect
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .abc import ExternalService, InternalService

InternalOrExternalService = type[InternalService] | type[ExternalService]
logger = logging.getLogger(__name__)


def _require_service_loader_attr(service_class: InternalOrExternalService):
    try:
        service_class.service_loader
    except AttributeError as e:
        raise ImproperlyConfigured("Missing service_loader on %s" % service_class) from e


def _get_kwonly_params_annotations_names(f):
    signature = inspect.signature(f)

    type_annotation_name = {}
    for name, param in signature.parameters.items():
        if param.kind != param.KEYWORD_ONLY:
            raise ImproperlyConfigured(
                "This decorator may only be applied to keyword only functions",
                f"Function {f} is not a keyword only arguments function",
                "Hint: Add `*` as the first parameter of the function",
            )
        type_annotation_name[param.annotation] = name
    return type_annotation_name


def _expect_all_service_classes_annotated(
    *service_classes: InternalOrExternalService, type_annotations: dict[type, str]
):
    for service_class in service_classes:
        if service_class not in type_annotations:
            raise ImproperlyConfigured(
                f"Missing type annotation for injectable external service {service_class}"
            )


def inject_service_at_runtime(*service_classes: InternalOrExternalService):
    """Decorator that wraps a keyword-only function that may receive only keyword arguments.
    This function must type-annotate the given `service_classes` as a parameter and expect to
    receive a instance of the service, not the class. At runtime will inject that service(s)
    automatically into the function, it also checks if we are on production. If so, and the
    injected service is not suitable for production this will raise a `ImproperlyConfiguredError`

    Example usage for the SMS service:
    ```
    # your_app/services.py
    from app.ext import di
    from app.ext.sms.abc import SMSExternalService

    @di.inject_service_at_runtime(SMSExternalService)
    def some_model_create(*, sms_service: SMSExternalService, something: int):
        sms_service.send()
    ```
    """
    for service_class in service_classes:
        _require_service_loader_attr(service_class)

    def decorator(f):
        type_annotations_names = _get_kwonly_params_annotations_names(f)
        _expect_all_service_classes_annotated(
            *service_classes, type_annotations=type_annotations_names
        )

        @functools.wraps(f)
        def injected_wrapper(**kwargs):
            for service_class in service_classes:
                service = service_class.service_loader()
                if settings.ON_PRODUCTION and not service.suitable_for_production:
                    raise ImproperlyConfigured(f"{service=} is not suitable for production")

                injection_kwarg_name = type_annotations_names[service_class]
                if injection_kwarg_name in kwargs:
                    logger.warning(
                        "Received the service on kwargs already, "
                        "no injection is going to be done"
                    )
                else:
                    logger.debug(f"Injecting {injection_kwarg_name} on func {f}")
                    kwargs[injection_kwarg_name] = service

            return f(**kwargs)

        return injected_wrapper

    return decorator
