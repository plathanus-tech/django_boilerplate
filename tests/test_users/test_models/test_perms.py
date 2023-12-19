import pytest

from users.models import User


class TrapObj:
    def has_obj_perm(self, *args, **kwargs):
        raise RuntimeError("Should not have been called")


@pytest.mark.django_db
def test_inactive_users_dont_have_perms(visitor_user: User):
    visitor_user.is_active = False
    assert visitor_user.has_perm("users.change_user") is False


@pytest.mark.django_db
def test_inactive_users_dont_trigger_object_level_validation(visitor_user: User):
    visitor_user.is_active = False
    assert visitor_user.has_perm("users.change_user", TrapObj()) is False


@pytest.mark.django_db
def test_superusers_always_have_perms(visitor_user: User):
    visitor_user.is_superuser = True
    assert visitor_user.has_perm("users.change_user")


@pytest.mark.django_db
def test_superusers_dont_trigger_object_level_validation(visitor_user: User):
    visitor_user.is_superuser = True
    assert visitor_user.has_perm("users.change_user", TrapObj()) is True


@pytest.mark.django_db
def test_not_passing_object_will_not_trigger_object_validation(visitor_user: User):
    visitor_user.is_active = True
    visitor_user.is_superuser = False
    assert visitor_user.has_perm("users.change_user", obj=None)


@pytest.mark.django_db
def test_normal_users_triggers_generic_object_level_validation(visitor_user: User):
    visitor_user.is_active = True
    visitor_user.is_superuser = False
    with pytest.raises(RuntimeError):
        visitor_user.has_perm("users.change_user", TrapObj())


class TrapObjSpecific:
    def has_change_obj_perm(self, *args, **kwargs):
        raise RuntimeError("Should not have been called")


@pytest.mark.django_db
def test_normal_users_triggers_specific_object_level_validation(visitor_user: User):
    visitor_user.is_active = True
    visitor_user.is_superuser = False
    with pytest.raises(RuntimeError):
        visitor_user.has_perm("users.change_user", TrapObjSpecific())


class TrapObjSpecificAndGeneric:
    def has_obj_perm(self, *args, **kwargs):
        raise ValueError("Shouldn't be called")

    def has_change_obj_perm(self, *args, **kwargs):
        return False


@pytest.mark.django_db
def test_normal_users_triggers_specific_object_level_and_not_generic_validation(visitor_user: User):
    visitor_user.is_active = True
    visitor_user.is_superuser = False

    assert visitor_user.has_perm("users.change_user", TrapObjSpecificAndGeneric()) is False


class ObjWithNoObjLevelPermCheck:
    ...


@pytest.mark.django_db
def test_normal_users_validation_is_not_performed_on_objs_that_dont_implement_it(
    visitor_user: User,
):
    visitor_user.is_active = True
    visitor_user.is_superuser = False

    assert visitor_user.has_perm("users.change_user", ObjWithNoObjLevelPermCheck()) is True
