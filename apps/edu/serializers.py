from typing import Any, Optional

from django.forms import BooleanField, IntegerField, ValidationError

from rest_framework.serializers import (
    Serializer,
    EmailField,
    CharField,
    ModelSerializer,
    SerializerMethodField,
    PrimaryKeyRelatedField,
)

from apps.auth.models import (
    EMAIL_FIELD_MAX_LENGTH,
    PASSWORD_FIELD_MAX_LENGTH,
    CustomUser,
)
from apps.auth.serializers import UserInfoSerializer
from apps.edu.models import Course, Lesson
from apps.edu.validators import indentation_validator


class CourseSerializer(ModelSerializer):
    """
    Serializer for Course model
    """

    id = CharField(read_only=True)
    title = CharField(required=True, max_length=255)
    description = CharField(required=True)
    owner = UserInfoSerializer(read_only=True)
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "owner",
            "lessons_count",
        )

    def get_lessons_count(self, obj: Course) -> int:
        return obj.lessons.filter(deleted_at__isnull=True).count()


class LessonSerializer(ModelSerializer):
    """
    Serializer for Lesson model
    """

    id = CharField(read_only=True)
    course = PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)
    title = CharField(required=True, max_length=255)
    content = CharField(required=True)
    order = IntegerField(required=True)
    indentation = IntegerField(required=True, validators=(indentation_validator,))
    is_published = BooleanField(required=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "course",
            "title",
            "content",
            "order",
            "indentation",
            "is_published",
        )
