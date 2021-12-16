from users.models import User


def test_str_user_is_equal_to_its_email(user: User):
    assert str(user) == user.email


def test_user_full_name_property_returns_fname_space_lname(user: User):
    assert user.full_name == f"{user.first_name} {user.last_name}"
