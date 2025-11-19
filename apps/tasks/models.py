from django.db.models import CharField, TextField, ForeignKey, CASCADE, ManyToManyField

from apps.abstract.models import AbstractBaseModel
from apps.auth.models import CustomUser


class Project(AbstractBaseModel):
    """
    Model representing a project.
    """

    NAME_MAX_LENGTH: int = 255

    name = CharField(max_length=NAME_MAX_LENGTH)
    description = TextField()

    author = ForeignKey(CustomUser, on_delete=CASCADE)
    users = ManyToManyField(CustomUser, related_name="projects")

class Task(AbstractBaseModel):
    """
    Model representing a task within a project.
    """

    TITLE_MAX_LENGTH: int = 255

    title = CharField(max_length=TITLE_MAX_LENGTH)
    description = TextField()
    status = CharField(max_length=50)

    project = ForeignKey(
        Project, 
        on_delete=CASCADE, 
        related_name="tasks"
    )

    assignees = ManyToManyField(
        CustomUser, 
        related_name="UserTask",
        through_fields=("task", "user"),
    )

    def get_status_as_dict(self) -> dict[str, int | str]:
        """
        Get the status of the task as a dictionary.

        Returns:
            dict[str, str]: A dictionary containing the status of the task.
        """

        return {
            "id": self.id,
            "title": self.title,
            "status": self.status
        }