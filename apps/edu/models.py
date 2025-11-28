from django.db.models import (
    CharField,
    TextField,
    BooleanField,
    DateTimeField,
    ForeignKey,
    DecimalField,
    PositiveSmallIntegerField,
    CASCADE,
)

from apps.abstract.models import AbstractBaseModel
from apps.auth.models import CustomUser


TITLE_MAX_LENGHT: int = 255


class Course(AbstractBaseModel):
    """
    Model representing a Course in the educational platform.
    """
    
    title = CharField(max_length=TITLE_MAX_LENGHT)
    is_active = BooleanField(default=True)
    description = TextField(blank=True, null=True)
    owner = ForeignKey(CustomUser, on_delete=CASCADE, related_name="owned_courses")

class Lesson(AbstractBaseModel):
    """
    Model representing a Lesson within a Course.
    """
    
    ORDER_MAX_DIGITS: int = 5
    ORDER_DECIMAL_PLACES: int = 2
    INDENTATION_MAX_VALUE: int = 5

    course = ForeignKey(Course, on_delete=CASCADE, related_name="lessons")
    title = CharField(max_length=TITLE_MAX_LENGHT)
    content = TextField()
    order = DecimalField(max_digits=ORDER_MAX_DIGITS, decimal_places=ORDER_DECIMAL_PLACES)
    indentation = PositiveSmallIntegerField(max_value=INDENTATION_MAX_VALUE)
    is_published = BooleanField(default=False)



