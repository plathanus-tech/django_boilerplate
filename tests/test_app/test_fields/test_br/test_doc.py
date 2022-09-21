from app import validators
from app.fields.br import doc


class DummyField(doc.BrazilianDocBaseField):
    mask_max_length: int = 10
    no_mask_max_length: int = 8
    widget_mask: str = "00000000-0"
    validator_class = validators.br.doc.BrazilianDocBaseValidator


def test_brazilian_doc_base_field_widgets_attrs():
    field = DummyField()
    attrs = field.widget_attrs(field.widget)
    assert "maxlength" in attrs
    assert "minlength" in attrs
    assert "data-mask" in attrs


def test_brazilian_doc_base_field_to_python():
    field = DummyField(keep_mask=True)
    value = "1234567-89"
    new_value = field.to_python(value)
    assert new_value == value

    field = DummyField(keep_mask=False)
    assert field.to_python(value) == "123456789"
