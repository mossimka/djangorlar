from  django.contrib.admin import register, ModelAdmin

from apps.tasks.models import Project

@register(Project)
class projectAdmin(ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)