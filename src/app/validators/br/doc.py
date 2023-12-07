from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from validate_docbr import (
    CNH,
    CNPJ,
    CNS,
    CPF,
    PIS,
    RENAVAM,
    BaseDoc,
    Certidao,
    TituloEleitoral,
)

if TYPE_CHECKING:
    from django_stubs_ext import StrOrPromise


@deconstructible
class BrazilianDocBaseValidator:
    message: "StrOrPromise"
    validator: BaseDoc

    def __call__(self, value):
        if not self.validator.validate(value):
            raise ValidationError(self.message, code="invalid")


class CertificateValidator(BrazilianDocBaseValidator):
    """Validator for birth/marriage/death Certificate(Certidão) document"""

    message = _("Invalid Certificate")
    validator = Certidao()


class CnhValidator(BrazilianDocBaseValidator):
    """Validator for the CNH document"""

    message = _("Invalid CNH")
    validator = CNH()


class CnpjValidator(BrazilianDocBaseValidator):
    """Validator for the CNPJ document"""

    message = _("Invalid CNPJ")
    validator = CNPJ()


class CnsValidator(BrazilianDocBaseValidator):
    """Validator for the CNH document"""

    message = _("Invalid CNS")
    validator = CNS()


class CpfValidator(BrazilianDocBaseValidator):
    """Validator for the CPF document"""

    message = _("Invalid CPF")
    validator = CPF()


class CpfCnpjValidator(BrazilianDocBaseValidator):
    """Validator for the CPF or CNPJ document"""

    message = _("Invalid CPF/CNPJ")

    def __call__(self, value):
        if not any([CPF().validate(value), CNPJ().validate(value)]):
            raise ValidationError(self.message, code="invalid")


class PisValidator(BrazilianDocBaseValidator):
    """Validator for the PIS document"""

    message = _("Invalid PIS")
    validator = PIS()


class RenavamValidator(BrazilianDocBaseValidator):
    """Validator for the Renavam document"""

    message = _("Invalid RENAVAM")
    validator = RENAVAM()


class VoterRegistrationValidator(BrazilianDocBaseValidator):
    """Validator for the Voter Registration(Titulo Eleitor) document"""

    message = _("Invalid Voter Registration")
    validator = TituloEleitoral()
