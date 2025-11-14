from rest_framework.serializers import ModelSerializer

from apps.auth.models import CustomUser


class UserSerializer(ModelSerializer):
    """
    Serializer for CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
        ]