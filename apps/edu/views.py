from typing import Any

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.edu.models import Course, Lesson
from apps.edu.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ViewSet):
    """
    View set for managing Course instances.    
    """

    permission_classes = (AllowAny,)

    @action(
        methods=["get",],
        detail=False,
        serializer_class=CourseSerializer,
        url_name="list",
        url_path="courses",
    )
    def list    