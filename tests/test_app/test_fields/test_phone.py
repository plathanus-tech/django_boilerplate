from typing import Optional

import pytest

from app.forms.fields import phone


def test_international_phone_number_field_widget_attrs():
    field = phone.InternationalPhoneNumberField()
    attrs = field.widget_attrs(field.widget)
    assert "data-mask" in attrs


@pytest.mark.parametrize(
    "region,in_phone,out_phone,scenario",
    (
        [None, "+55 48 991234-5678", "+55489912345678", "No region. International format"],
        ["BR", "48 9 1234-5678", "+5548912345678", "With region. National format"],
        ["BR", "55 48 9 12345678", "+5548912345678", "With region. International format"],
    ),
)
def test_international_phone_number_field_to_python(
    region: Optional[str], in_phone: str, out_phone: str, scenario: str
):
    field = phone.InternationalPhoneNumberField(region=region)
    assert out_phone == field.to_python(in_phone), scenario
