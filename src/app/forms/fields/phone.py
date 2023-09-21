from typing import Optional

import phonenumbers
from django import forms
from django.utils.translation import gettext_lazy as _


class InternationalPhoneNumberField(forms.CharField):
    region: Optional[str]
    output_format: int

    def __init__(
        self,
        region: Optional[str] = None,
        output_format: int = phonenumbers.PhoneNumberFormat.E164,
        input_mask: Optional[str] = None,
        **charfield_kwargs,
    ):
        """Form Field that validates and outputs phone numbers on a specific format.
        The arguments are passed directly to the phonenumbers parse/format_number functions."""

        self.region = region
        self.output_format = output_format
        self.input_mask = input_mask

        charfield_kwargs.setdefault("max_length", 20)
        super().__init__(**charfield_kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return None
        try:
            phone = phonenumbers.parse(value, region=self.region)
        except phonenumbers.NumberParseException as e:
            raise forms.ValidationError(
                _("Invalid phone number. Original error message was: %s") % e._msg
            )
        return phonenumbers.format_number(phone, num_format=self.output_format)

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "data-mask": self.input_mask or f"+{'0' * self.max_length}",
        }
