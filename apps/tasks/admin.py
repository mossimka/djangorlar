

from typing import Optional
from django.contrib.admin import ModelAdmin, register
from django.core.handlers.wsgi import WSGIRequest

from .models import Task, Project, UserTask


@register(Project)
class ProjectAdmin(ModelAdmin):
    """
    Project admin configuration class.
    """

    list_per_page = 25

    list_display = (
        'id', 
        'name', 
        'author',
        'created_at',
    )
    list_display_links = (
        'id',
    )
    search_fields = (
        'name',
        'id',
    )
    ordering = (
        '-updated_at',
    )
    list_filter = (
        'updated_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'deleted_at',
    )
    save_on_top = True
    fieldsets = (
        (
            "Project Information",
            {
                'fields': (
                    'name',
                    'author',
                    'users',
                )
            }
        ),
        (
            "Timestamps",
            {
                'fields': (
                    'created_at',
                    'updated_at',
                    'deleted_at',
                )
            }
        )
    )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        return False

    def has_delete_permission(self, request: WSGIRequest, obj: Optional[Project] = None) -> bool:
        return False

    def has_change_permission(self, request: WSGIRequest, obj: Optional[Project] = None) -> bool:
        return False



@register(Task)
class TaskAdmin(ModelAdmin):
    """
    Task admin configuration class.
    """

    ...

@register(UserTask)
class UserTaskAdmin(ModelAdmin):
    """
    UserTask admin configuration class.
    """

    ...
