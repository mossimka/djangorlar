from typing import Any, Optional

from rest_framework.serializers import Serializer, EmailField, CharField, ValidationError

from apps.auth.models import EMAIL_FIELD_MAX_LENGTH, PASSWORD_FIELD_MAX_LENGTH, CustomUser


class UserLoginSerializer(Serializer):
    """
    Serializer for user login
    """

    email = EmailField(
        required=True,
        max_length=EMAIL_FIELD_MAX_LENGTH,
    )
    password = CharField(
        required=True,
        max_length=PASSWORD_FIELD_MAX_LENGTH,
    )

    class Meta:
        fields = (
            "email",
            "password",
        )


    def validate(self, attrs: dict[str, Any]):
        email: str = attrs["email"]
        password: str = attrs["password"]

        user: Optional[CustomUser] = CustomUser.objects.filter(
            email=email
        ).first()

        if not user:
            raise ValidationError(
                detail={
                    "email": "User with this email does not exist."
                }
            )

        if not user.check_password(raw_password=password):
            raise ValidationError(
                detail={
                    "password": "Incorrect password."
                }
            )
    
        attrs["user"] = user

        return super().validate(attrs)
    
class RefreshTokenSerializer(Serializer):
    """
    Serializer for refreshing access token
    """

    refresh = CharField(
        required=True,
    )

    class Meta:
        fields = (
            "refresh",
        )

class UserInfoSerializer(Serializer):
    """
    Serializer for user information
    """

    user_id = CharField(
        read_only=True,
    )
    email = EmailField(
        read_only=True,
    )
    username = CharField(
        read_only=True,
    )

    class Meta:
        fields = (
            "user_id",
            "email",
            "username",
        )