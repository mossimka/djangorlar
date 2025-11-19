from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.tasks.models import Project, Task
from apps.abstract.serializers import CustomUserForeignSerializer


class ProjectBaseSerializer(ModelSerializer):
    """
    Base serializer for the Project model.
    """

    author = CustomUserForeignSerializer()

    class Meta:
        """
        Customize the ProjectBaseSerializer metadata.
        """

        model = Project
        fields = "__all__"


class ProjectListSerializer(ProjectBaseSerializer):
    """
    Serializer for the Project model.
    """

    users_count = SerializerMethodField(
        help_text="The number of users associated with the project.",
        method_name="get_users_count",
    )

    author = CustomUserForeignSerializer()

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

class ProjectCreateSerializer(ProjectBaseSerializer):
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

class ProjectPatchSerializer(ProjectBaseSerializer):
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



class TaskBaseSerializer(ModelSerializer):
    """
    Base serializer for the Task model.
    """

    asignee = CustomUserForeignSerializer()

    class Meta:
        """
        Customize the TaskBaseSerializer metadata.
        """

        model = Task
        fields = "__all__"

    def get_status(self, obj: Task) -> dict[str, int | str]:
        """
        Get the status of the task as a dictionary.

        Parameters:
            obj (Task): The task instance.
        Returns:
            dict[str, str]: A dictionary containing the status of the task.
        """

        return obj.get_status_as_dict()


class TaskListSerializer(TaskBaseSerializer):   
    """
    Serializer for the Task model.
    """

    assignees = CustomUserForeignSerializer(many=True)

    class Meta:
        """
        Customize the TaskSerializer metadata.
        """

        model = Task
        fields = (
            "id",
            "title",
            "description",
            "project",
            "assignees",
        )

    
class TaskCreateSerializer(TaskBaseSerializer):
    """
    Serializer for creating a new Task.
    """

    project: int = 

    class Meta:
        """
        Customize the TaskCreateSerializer metadata.
        """

        model = Task
        fields = (
            "id",
            "title",
            "description",
            "project",
            "status",
            "assignees",
        )