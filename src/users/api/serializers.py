from django.contrib.auth import get_user_model
from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("first_name", "last_name", "email", "is_active")


class TokenSerializer(serializers.Serializer):
    user = UserSerializer()
    access_token = serializers.CharField(required=True)
    token_type = serializers.CharField(default="Token")
