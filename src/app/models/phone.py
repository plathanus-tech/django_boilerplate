from typing import Optional

import phonenumbers
from django.db.models import CharField

from app import fields


class InternationalPhoneNumberField(CharField):
    """Model field for International Phone Numbers."""

    def __init__(
        self,
        *,
        region: Optional[str] = None,
        output_format: int = phonenumbers.PhoneNumberFormat.E164,
        input_mask: Optional[str] = None,
        **charfield_kwargs,
    ):
        self.region = region or "BR"
        self.output_format = output_format
        self.input_mask = input_mask or "+00 (00) 00000-0000"
        charfield_kwargs.setdefault("max_length", 20)
        super().__init__(**charfield_kwargs)

    def formfield(self, **kwargs):
        meta = phonenumbers.phonemetadata.PhoneMetadata.metadata_for_region(self.region)

        return super().formfield(
            **{
                **kwargs,
                "form_class": fields.InternationalPhoneNumberField,
                "region": self.region,
                "output_format": self.output_format,
                "input_mask": self.input_mask,
                "initial": f"+{meta.country_code}" if meta else "+",
            }
        )
