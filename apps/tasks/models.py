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
