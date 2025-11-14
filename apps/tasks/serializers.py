from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.tasks.models import Project
from apps.abstract.serializers import UserSerializer


class ProjectListSerializer(ModelSerializer):
    """
    Serializer for the Project model.
    """

    users_count = SerializerMethodField(
        help_text="The number of users associated with the project.",

    )

    author = UserSerializer()

    class Meta:
        """
        Customize the ProjectSerializer metadata.
        """

        model = Project
        fields = (
            "id",
            "name",
            "description",
            "users_count",
        )

    def get_users_count(self, obj: Project) -> int:
        """
        Get the count of users associated with the project.

        Parameters:
            obj (Project): The project instance.

        Returns:
            int: The number of users associated with the project.
        """

        return getattr(obj, "users_count", 0)

class ProjectCreateSerializer(ModelSerializer):
    """
    Serializer for creating a new Project.
    """

    class Meta:
        """
        Customize the ProjectCreateSerializer metadata.
        """

        model = Project
        fields = (
            "id",
            "name",
            "author",
            "description",
        )

class ProjectPatchSerializer(ModelSerializer):
    """
    Serializer for updating an existing Project.
    """

    class Meta:
        """
        Customize the ProjectUpdateSerializer metadata.
        """

        model = Project
        fields = (
            "name",
            "description",
        )