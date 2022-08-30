from typing import Type

from django.db.models import CharField

from app import fields


class BrazilianDocBaseField(CharField):
    """Base class for all Brazilian documents model fields.
    Do not use this class directly on your models!"""

    form_class: Type[fields.br.doc.BrazilianDocBaseField]

    def __init__(self, *args, **kwargs):
        """Checkout CharField args kwargs"""
        kwargs["max_length"] = self.form_class.no_mask_max_length
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(**{"form_class": self.form_class, **kwargs})


class CertificateField(BrazilianDocBaseField):
    """Model field for a birth/marriage/death Certificate (Certidao) document"""

    form_class = fields.br.doc.CertificateField


class CnhField(BrazilianDocBaseField):
    """Model field for a CNH document"""

    form_class = fields.br.doc.CnhField


class CnpjField(BrazilianDocBaseField):
    """Model field for a CNPJ document"""

    form_class = fields.br.doc.CnpjField


class CnsField(BrazilianDocBaseField):
    """Model field for a CNS document"""

    form_class = fields.br.doc.CnsField


class CpfField(BrazilianDocBaseField):
    """Model field for a CPF document"""

    form_class = fields.br.doc.CpfField


class CpfCnpjField(BrazilianDocBaseField):
    """Model field for a Cpf/Cnpj document"""

    form_class = fields.br.doc.CpfCnpjField


class PisField(BrazilianDocBaseField):
    """Model field for a PIS document"""

    form_class = fields.br.doc.PisField


class RenavamField(BrazilianDocBaseField):
    """Model field for a RENAVAM document"""

    form_class = fields.br.doc.RenavamField


class VoterRegistrationField(BrazilianDocBaseField):
    """Model field for a Voter Registration(Titulo Eleitor) document"""

    form_class = fields.br.doc.VoterRegistrationField
