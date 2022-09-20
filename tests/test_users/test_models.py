from users.models import User


def testUserStrReturnsEmail(admin_user: User):
    assert str(admin_user) == admin_user.email
