import uuid

from users.models import User


def user_delete_account(user: User):
    user.is_active = False
    user.email = uuid.uuid4().hex + "@deleted-account.com"
    user.save()
