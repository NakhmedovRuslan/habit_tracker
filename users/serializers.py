from rest_framework import serializers

from users.models import CustomUser


class CustomUsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "password",
            "tg_chat_id",
            "email",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
