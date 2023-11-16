from rest_framework import serializers

from app.consts.i18n import Language, TimeZoneName
from app.drf.fields import create_choice_human_field
from users.models import User


class AuthenticationInputSchema(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class StaticTokenSchema(serializers.Serializer):
    type = serializers.CharField(default="Token")
    access = serializers.CharField()
    refresh = serializers.CharField(default=None)


class JwtTokenSchema(serializers.Serializer):
    type = serializers.CharField(default="Bearer")
    access = serializers.CharField()
    refresh = serializers.CharField()


LanguageChoiceField = create_choice_human_field(Language)
TimeZoneNameChoiceField = create_choice_human_field(TimeZoneName)


class _AuthenticationOutputSchema(serializers.ModelSerializer):
    language_code = LanguageChoiceField()
    time_zone = TimeZoneNameChoiceField()
    token = serializers.CharField(default=None)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "language_code",
            "time_zone",
            "token",
        )


class TokenAuthenticationOutputSchema(_AuthenticationOutputSchema):
    token = StaticTokenSchema()


class JwtTokenAuthenticationOutputSchema(_AuthenticationOutputSchema):
    token = JwtTokenSchema()
