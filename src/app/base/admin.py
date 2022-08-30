def no_permission(*args, **kwargs) -> bool:
    """A callable that will always return False"""
    return False


class ReadOnlyAdminMixin:
    """A read-only admin. It must be inherited before the `admin.ModelAdmin` due to python's MRO."""

    has_add_permission = no_permission
    has_delete_permission = no_permission
    has_change_permission = no_permission
