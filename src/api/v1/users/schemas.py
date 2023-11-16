from rest_framework import serializers

from api.v1.auth.schemas import LanguageChoiceField, TimeZoneNameChoiceField
from users.models import User


class CurrentUserOutputSchema(serializers.ModelSerializer):
    language_code = LanguageChoiceField()
    time_zone = TimeZoneNameChoiceField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "notification_token",
            "language_code",
            "time_zone",
            "date_joined",
            "is_staff",
            "is_superuser",
        )
