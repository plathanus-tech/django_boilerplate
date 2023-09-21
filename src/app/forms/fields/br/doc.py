from typing import Type

from django import forms

try:
    from validate_docbr import BaseDoc
except ImportError as e:
    raise ImportError(
        "`validate-docbr` is not installed. This is an optional dependency.",
        "Did your forgot to install all the dependencies using: `pdm install -G :all`?"
        "Or maybe if you only want to add this dependency, run `pdm install -G brdocs`",
    ) from e

from app import validators


class BrazilianDocBaseField(forms.CharField):
    """Base class for Brazilian Documents fields. Use validate-docbr classes to wrap the validation on subclasses.
    Do not use this class on a Form directly!"""

    keep_mask: bool
    mask_max_length: int
    no_mask_max_length: int
    validator_class: Type[validators.br.doc.BrazilianDocBaseValidator]
    widget_mask: str

    def __init__(self, *, keep_mask: bool = False, **charfield_kwargs) -> None:
        self.keep_mask = keep_mask
        charfield_kwargs["max_length"] = (
            self.mask_max_length if keep_mask else self.no_mask_max_length
        )
        super().__init__(**charfield_kwargs)
        self.validators.append(self.validator_class())

    def to_python(self, value):
        value = super().to_python(value)
        if not value or self.keep_mask:
            return value
        return BaseDoc()._only_digits(value)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update(
            {
                "maxlength": self.mask_max_length,
                "minlength": self.no_mask_max_length,
                "data-mask": self.widget_mask,
            }
        )
        return attrs


class CertificateField(BrazilianDocBaseField):
    """Form field for a birth/marriage/death certificate (Certidao) document"""

    mask_max_length = 40
    no_mask_max_length = 32
    validator_class = validators.br.doc.CertificateValidator
    widget_mask = "000000 00 00 0000 0 00000 000 0000000-00"


class CpfField(BrazilianDocBaseField):
    """Form field for a CPF document"""

    mask_max_length = 14
    no_mask_max_length = 11
    validator_class = validators.br.doc.CpfValidator
    widget_mask = "000.000.000-00"


class CnpjField(BrazilianDocBaseField):
    """Form field for a CNPJ document"""

    mask_max_length = 18
    no_mask_max_length = 14
    validator_class = validators.br.doc.CnpjValidator
    widget_mask = "00.000.000/0000-00"


class CpfCnpjField(BrazilianDocBaseField):
    """Form field for a CPF or CNPJ document"""

    mask_max_length = 18
    no_mask_max_length = 14
    validator_class = validators.br.doc.CpfCnpjValidator
    widget_mask = "000000000000000000"


class CnhField(BrazilianDocBaseField):
    """Form field for a CNH document"""

    mask_max_length = 11
    no_mask_max_length = 11
    validator_class = validators.br.doc.CnhValidator
    widget_mask = "00000000000"


class CnsField(BrazilianDocBaseField):
    """Form field for a CNS document"""

    mask_max_length = 18
    no_mask_max_length = 15
    validator_class = validators.br.doc.CnsValidator
    widget_mask = "000 0000 0000 0000"


class PisField(BrazilianDocBaseField):
    """Form field for a PIS document"""

    mask_max_length = 14
    no_mask_max_length = 11
    validator_class = validators.br.doc.PisValidator
    widget_mask = "000.00000.00-0"


class RenavamField(BrazilianDocBaseField):
    """Form field for a RENAVAM document"""

    mask_max_length = 11
    no_mask_max_length = 11
    validator_class = validators.br.doc.RenavamValidator
    widget_mask = "00000000000"


class VoterRegistrationField(BrazilianDocBaseField):
    """Form field for a Voter Registration (Titulo Eleitor) document"""

    mask_max_length = 12
    no_mask_max_length = 12
    validator_class = validators.br.doc.VoterRegistrationValidator
    widget_mask = "000000000000"
