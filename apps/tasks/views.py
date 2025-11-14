from typing import Any


from django.db.models import (
    QuerySet, 
    Count,
)

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)

from apps.tasks.models import Project
from apps.tasks.serializers import (
    ProjectListSerializer, 
    ProjectCreateSerializer,
    ProjectPatchSerializer,
)


class ProjectViewSet(ViewSet):
    """
    ViewSet for project handling endpoints.
    """

    def list(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        """
        Hadle GET requests for listing projects.

        Parametrs:
            request (Request): The incoming request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: The response object containing the list of projects.

        """

        projects: QuerySet[Project] = Project.objects.annotate(
            users_count=Count("users", distinct=True)
        ).all()

        serializer: ProjectListSerializer = ProjectListSerializer(projects, many=True)

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )
    

    def create(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        """
        Handle POST requests for creating a new project.

        Parameters:
            request (Request): The incoming request object. 
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: The response object confirming project creation.
        """

        serializer: ProjectCreateSerializer = ProjectCreateSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                data={"errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(
            data=serializer.data,
            status=HTTP_201_CREATED,
        )

    def partial_update(
        self, 
        request: Request,
        *args: Any, 
        **kwargs: dict[str, Any]
    ) -> Response:
        """
        Handle PATCH requests for updating a project.

        Parameters:
            request (Request): The incoming request object. 
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: The response object confirming project update.
        """

        try:
            project: Project = Project.objects.get(id=kwargs.get("pk"))
        except Project.DoesNotExist:
            return Response(
                data={"error": "Project not found"},
                status=HTTP_404_NOT_FOUND,
            )

        serializer: ProjectPatchSerializer = ProjectPatchSerializer(
            project,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                data={"errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )
    
    def destroy(
        self,
        request: Request,
        *args: Any,
        **kwargs: dict[str, Any]
    ) -> Response:
        """
        Handle DELETE requests for deleting a project.

        Parameters:
            request (Request): The incoming request object. 
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: The response object confirming project deletion.
        """
        
        try:
            project: Project = Project.objects.get(id=kwargs.get("pk"))
        except Project.DoesNotExist:
            return Response(
                data={"error": "Project not found"},
                status=HTTP_404_NOT_FOUND,
            )

        project.delete()

        return Response(
            data={"message": "Project deleted successfully."},
            status=HTTP_204_NO_CONTENT,
        )