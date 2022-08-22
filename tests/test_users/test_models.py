from users.models import User


def testUserStrReturnsEmail(admin_user: User):
    assert str(admin_user) == admin_user.email


def testUserFullNameReturnsFirstLastName(admin_user: User):
    admin_user.first_name = "John"
    admin_user.last_name = "Doe"

    assert admin_user.full_name == "John Doe"


def testUserGetShortNameReturnsFullName(admin_user: User):
    admin_user.first_name = "John"
    admin_user.last_name = "Doe"

    assert admin_user.get_short_name() == "John Doe"
