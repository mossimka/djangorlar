from django.db.models import (
    CharField,
    TextField,
    IntegerField,
    ForeignKey,
    ManyToManyField,
    CASCADE,
    PROTECT,
    UniqueConstraint,
)

from django.contrib.auth.models import User
from apps.abstract.models import AbstractBaseModel


NAME_MAX_LENGTH = 255


class Project(AbstractBaseModel):
    """
    Represents a project in the system
    """

    name = CharField(
        max_length=NAME_MAX_LENGTH,
    )
    author = ForeignKey(
        to=User,
        on_delete=PROTECT,
        related_name='owned_projects',
    )
    members = ManyToManyField(
        to=User,
        blank=True,
        related_name='joined_projects',
    )

    def __repr__(self):
        return f"Project: {self.name} (ID: {self.id})"

    def __str__(self):
        return self.name


class Task(AbstractBaseModel):
    """
    Represents a task in the system.
    """

    STATUS_TODO = 1
    STATUS_TODO_LABEL = 'To Do'
    STATUS_IN_PROGRESS = 2
    STATUS_IN_PROGRESS_LABEL = 'In Progress'
    STATUS_DONE = 3
    STATUS_DONE_LABEL = 'Done'

    STATUS_CHOICES = (
        (STATUS_TODO, STATUS_TODO_LABEL),
        (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS_LABEL),
        (STATUS_DONE, STATUS_DONE_LABEL),
    )

    title = CharField(
        max_length=NAME_MAX_LENGTH,
        db_index=True,
    )

    description = TextField(
        blank=True, 
        null=True
    )

    status = IntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_TODO,
    )

    parent = ForeignKey(
        to='self',
        on_delete=CASCADE,
        blank=True,
        null=True
    )

    project = ForeignKey(
        to=Project,
        on_delete=CASCADE,
    )

    assignees = ManyToManyField(
        to=User,
        through='UserTask',
        through_fields=('task', 'user'),
        blank=True,
    )


class UserTask(AbstractBaseModel):
    """
    Intermediate model for the relation between User and Task
    """

    user = ForeignKey(
        to=User,
        on_delete=CASCADE,
    )
    task = ForeignKey(
        to=Task,
        on_delete=CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'task'],
                name='unique_user_task'
            )
        ]
        