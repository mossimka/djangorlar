from django.urls import include, path

from rest_framework.routers import DefaultRouter

from apps.tasks.views import ProjectViewSet


router: DefaultRouter = DefaultRouter(
    trailing_slash=False,
)

router.register(
    prefix="projects",
    viewset=ProjectViewSet,
    basename="projects",
)

urlpatterns = [
    path("v1/", include(router.urls)),
]
