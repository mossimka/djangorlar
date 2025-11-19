from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from apps.tasks.models import Project


class IsUserInProject(BasePermission):
    """
    Custom permission to check if the user is part of the project.
    """
    
    def has_object_permission(
        self,
        request: Request,
        view: ViewSet,
        obj: Project,
    ) -> bool:
        project_id: int = obj.id if isinstance(obj, Project) else obj

        if  not isinstance(project_id, int):
            return False
        
        return Project.objects.filter(
            users__id=request.user.id,
            id=project_id
        ).exists()