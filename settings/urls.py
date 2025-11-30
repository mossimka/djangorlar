from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from settings.base import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.auth.urls")),
    path("api/edu/", include("apps.edu.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += static(prefix=STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(prefix=MEDIA_URL, document_root=MEDIA_ROOT)
