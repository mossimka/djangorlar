from django.contrib.admin import register, ModelAdmin

from apps.auth.models import CustomUser


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
    )
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_staff", "department", "role")
    ordering = ("-date_joined",)

    
