from typing import Any

from django.shortcuts import render
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.edu.models import Course, Lesson
from apps.edu.serializers import CourseSerializer, LessonSerializer
from apps.edu.permissions import IsOwner, IsCourseOwner


class CourseViewSet(ViewSet):
    """
    View set for managing Course instances.
    """

    permission_classes = (IsAuthenticated,)

    def list(slef, request: Request) -> Response:
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
            return Response(serializer.data, status=HTTP_200_OK)
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
        methods=["post",],
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
        methods=["post",],
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
        methods=["get",],
        permission_classes=[AllowAny,],
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
    
    