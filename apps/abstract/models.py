from typing import Any
from django.db.models import Model, DateTimeField, Manager
from datetime import timezone


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class AbstractBaseModel(Model):
    """
    Abstract base model for all models in the application.
    """
    
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = Manager()  # Includes soft-deleted objects

    class Meta:
        abstract = True

    def delete(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        self.deleted_at = timezone.now()
        self.save()