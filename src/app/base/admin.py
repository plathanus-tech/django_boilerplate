from django.contrib.admin.options import BaseModelAdmin


def no_permission(*args, **kwargs) -> bool:
    """A callable that will always return False"""
    return False


class ReadOnlyAdminMixin:
    """A read-only admin"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.has_add_permission = no_permission
        self.has_delete_permission = no_permission
        self.has_change_permission = no_permission
