import pytest
from typing import Dict, Generator
from users.models import User


@pytest.fixture
def user_email() -> str:
    return "junior@gmail.com"


@pytest.fixture
def user_password() -> str:
    return "JuniorLikesPython"


@pytest.fixture
def user_first_name() -> str:
    return "Junior"


@pytest.fixture
def user_last_name() -> str:
    return "Smith"


@pytest.fixture
def staff_user(
    db,
    user_email: str,
    user_password: str,
    user_first_name: str,
    user_last_name: str,
) -> Generator[User, None, None]:
    user = User.objects.create_staffuser(
        email=user_email,
        password=user_password,
        first_name=user_first_name,
        last_name=user_last_name,
    )
    assert user.is_staff
    yield user
    user.delete()


@pytest.fixture
def user(staff_user: User) -> Generator[User, None, None]:
    """Shortcut for staff_user"""
    yield staff_user


@pytest.fixture
def non_staff_user(
    db,
    user_email: str,
    user_password: str,
    user_first_name: str,
    user_last_name: str,
) -> Generator[User, None, None]:
    user = User.objects.create_user(
        email=user_email,
        password=user_password,
        first_name=user_first_name,
        last_name=user_last_name,
    )
    assert not user.is_staff
    yield user
    user.delete()


@pytest.fixture
def superuser_user(
    db,
    user_email: str,
    user_password: str,
    user_first_name: str,
    user_last_name: str,
) -> Generator[User, None, None]:
    user = User.objects.create_superuser(
        email=user_email,
        password=user_password,
        first_name=user_first_name,
        last_name=user_last_name,
    )
    assert user.is_staff
    assert user.is_superuser
    yield user
    user.delete()


@pytest.fixture
def base_auth_payload() -> Dict[str, str]:
    return {
        "email": "",
        "password": "",
    }
