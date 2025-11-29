from typing import Any

from django.shortcuts import render
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.edu.models import Course, Lesson
from apps.edu.serializers import CourseSerializer, LessonSerializer
from apps.edu.permissions import IsOwner, IsCourseOwner


class CourseViewSet(ViewSet):
    """
    View set for managing Course instances.
    """

    # Добавили IsOwner, чтобы check_object_permissions работал корректно для update/destroy
    permission_classes = (IsAuthenticated, IsOwner)

    # --- Добавляем для Swagger ---
    def get_serializer_class(self):
        if self.action == "lessons":
            return LessonSerializer
        return CourseSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if serializer_class:
            kwargs.setdefault("context", {"request": self.request, "view": self})
            return serializer_class(*args, **kwargs)
        return None

    # -----------------------------

    def list(self, request: Request) -> Response:  # Исправлено slef -> self
        courses = Course.objects.all()

        is_active = request.query_params.get("is_active")
        if is_active is not None:
            courses = courses.filter(is_active=is_active.lower() == "true")

        courses = courses.annotate(lessons_count=Count("lessons"))

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request: Request) -> Response:
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request: Request, pk: int) -> Response:
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, course)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk: int) -> Response:
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, course)

        course.delete()
        return Response(status=HTTP_200_OK)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticated, IsOwner],
    )
    def activate(self, request: Request, pk: int) -> Response:
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, course)

        course.is_active = True
        course.save()
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticated, IsOwner],
    )
    def deactivate(self, request: Request, pk: int) -> Response:
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, course)

        course.is_active = False
        course.save()
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=["get"],
        permission_classes=[AllowAny],
        detail=True,
    )
    def lessons(self, request: Request, pk: int) -> Response:
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=HTTP_404_NOT_FOUND)

        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class LessonViewSet(ViewSet):
    """
    View set for managing Lesson instances.
    """

    permission_classes = (IsAuthenticated,)

    # --- Добавляем для Swagger ---
    def get_serializer_class(self):
        return LessonSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if serializer_class:
            kwargs.setdefault("context", {"request": self.request, "view": self})
            return serializer_class(*args, **kwargs)
        return None

    # -----------------------------

    def create(self, request: Request) -> Response:
        course_id = request.data.get("course")
        course = Course.objects.filter(id=course_id).first()
        if not course:
            return Response({"detail": "Course not found."}, status=HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, course)

        first = Lesson.objects.filter(course=course).order_by("order").first()
        order = first.order - 1 if first else 1

        serializer = LessonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(course=course, order=order)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(
        methods=["put"],
        detail=True,
    )
    def move(self, request, pk: int) -> Response:
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found."}, status=HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, lesson.course)

        before_id = request.data.get("before_lesson_id")

        if before_id:
            before = Lesson.objects.filter(
                pk=before_id
            ).first()
            if before:
                lesson.order = before.order - 1
        else:
            last = (
                Lesson.objects.filter(course=lesson.course).order_by("-order").first()
            )
            lesson.order = (last.order + 1) if last else 1

        lesson.save()
        serializer = LessonSerializer(lesson)
        return Response(
            {"detail": {"new_order": lesson.order, "lesson": serializer.data}},
            status=HTTP_200_OK,
        )

    def destroy(self, request: Request, pk: int) -> Response:
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found."}, status=HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, lesson.course)

        lesson.delete()
        return Response(status=HTTP_200_OK)
    
    @action(
        methods=["post"],
        permission_classes=[AllowAny],
        detail=True,
    )
    def publish(self, request: Request, pk: int) -> Response:
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"detial": "Lesson not found."}, status=HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, lesson.course)

        lesson.is_published = True
        lesson.save()
        serializer = LessonSerializer(lesson)
        return Response(serializer.data, status=HTTP_200_OK)
    
    @action(
        methods=["post"],
        permission_classes=[AllowAny],
        detail=True,
    )
    def unpublish(self, request: Request, pk: int) -> Response:
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"detial": "Lesson not found."}, status=HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, lesson.course)

        lesson.is_published = False
        lesson.save()
        serializer = LessonSerializer(lesson)
        return Response(serializer.data, status=HTTP_200_OK)