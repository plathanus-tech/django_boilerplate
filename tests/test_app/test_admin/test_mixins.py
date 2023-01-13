import pytest

from app.admin.mixins import ReadOnlyAdminMixin

attrs = [
    ("has_add_permission"),
    ("has_change_permission"),
    ("has_delete_permission"),
]


@pytest.mark.parametrize("attr", attrs)
def testReadOnlyAdminMixinHasAttributes(attr: str):
    admin = ReadOnlyAdminMixin()
    assert hasattr(admin, attr)


@pytest.mark.parametrize("attr", attrs)
def testReadOnlyAdminMixinAttributesWillReturnFalse(attr: str):
    admin = ReadOnlyAdminMixin()
    func = getattr(admin, attr)
    assert func() is False
