from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers

from users.models import User


class LoginSerializer(serializers.Serializer):
    user: User

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user: User = authenticate(**attrs)  # type: ignore
        if not user:
            raise serializers.ValidationError(_("Unable to login with the given credentials"))
        self.user = user
        return attrs

    class Meta:
        fields = ["email", "password"]


class LoggedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "date_joined"]


class LoginTokenSerializer(serializers.Serializer):
    user = LoggedUserSerializer()
    access = serializers.CharField()
    refresh = serializers.CharField()
    token_type = serializers.CharField()

    class Meta:
        fields = ["user", "access", "refresh", "token_type"]
