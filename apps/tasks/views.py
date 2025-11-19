from typing import Any


from django.db.models import (
    QuerySet, 
    Count,
)

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)
from rest_framework.decorators import api_view, action

from apps.tasks.models import Project
from apps.tasks.serializers import (
    ProjectListSerializer, 
    ProjectCreateSerializer,
    ProjectPatchSerializer,
    ProjectBaseSerializer,
    TaskListSerializer,
    TaskCreateSerializer,
)
from apps.tasks.permissions import IsUserInProject


class ProjectViewSet(ViewSet):
    """
    ViewSet for pro
ject handling endpoints.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectBaseSerializer

    def list(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        """
        Hadle GET requests for listing projects.

        Parametrs:
            request (Request): The incoming request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: The response object containinrg the list of projects.

        """

        projects: QuerySet[Project] = Project.objects.select_for_update()(
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

    def update(
        self,
        request: Request,
        *args: Any,
        **kwargs: dict[str, Any]
    ) -> Response:
        """
        Handle PUT requests for updating a project.

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
    
    @action(
        methods=["get"],
        detail=True,
        permission_classes=[IsAuthenticated, IsUserInProject,],
        url_path="tasks",
        url_name="tasks",
    )
    def get_tasks(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        """
        Handle GET requests for retrieving tasks of a specific project.

        Parameters:
            request (Request): The incoming request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: The response object containing the list of tasks for the project.
        """
        
        try:
            project: Project = Project.objects.get(id=kwargs.get("pk"))
        except Project.DoesNotExist:
            return Response(
                data={
                    "error": f"Project with id={kwargs.get('pk')} not found",

                },
                status=HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, project)

        tasks = project.tasks.all()
        serializer = TaskListSerializer(tasks, many=True)

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )
    
    @action (
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticated, IsUserInProject,],
        url_path="tasks",
        url_name="tasks",
    )
    def create_task(self, request: Request, *args: Any, **kwargs: dict[str, Any]) -> Response:
        """
        Handle POST requests for creating a new task within a specific project.

        Parameters:
            request (Request): The incoming request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: The response object confirming task creation.
        """

        try:
            project: Project = Project.objects.get(id=kwargs.get("pk"))
        except Project.DoesNotExist:
            return Response(
                data={
                    "error": f"Project with id={kwargs.get('pk')} not found",
                },
                status=HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, project)

        serializer: TaskCreateSerializer = TaskCreateSerializer(
            data=request.data,
            context={"id": project.id},
        )

        if not serializer.is_valid():
            return Response(
                data={"errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer.save(project=project)

        return Response(
            data=serializer.data,
            status=HTTP_201_CREATED,
        )

class TaskViewSet(ViewSet):
    pass