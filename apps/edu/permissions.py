from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access or edit it.
    """

    def has_object_permission(
        self, request: Request, view: ViewSet, obj: Any
    ) -> bool:
        """
        Check if the requesting user is the owner of the object.
        Args:
            request (Request): The incoming request object.
            view (ViewSet): The view set handling the request.
            obj (Any): The object being accessed.
        Returns:
            bool: True if the user is the owner, False otherwise.
        """

        return obj.owner == request.user
    

class IsCourseOwner(BasePermission):
    """
    Custom permission to only allow owners of a course to access or edit its lessons.
    """

    def has_object_permission(
            self,
            request: Request,
            view: ViewSet,
            obj: Any
    ) -> bool:
        """
        Check if the requesting user is the owner of the course associated with the lesson.
        Args:
            request (Request): The incoming request object.
            view (ViewSet): The view set handling the request.
            obj (Any): The lesson object being accessed.
        Returns:
            bool: True if the user is the owner of the course, False otherwise.
        """

        return obj.course.owner == request.user