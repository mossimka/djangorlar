from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from settings.base import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL


# --------------------------------------------------------
# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="API docs",
        contact=openapi.Contact(email="you@example.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.auth.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]

urlpatterns += static(prefix=STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(prefix=MEDIA_URL, document_root=MEDIA_ROOT)
