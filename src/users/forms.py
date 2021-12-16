from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from .models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)
