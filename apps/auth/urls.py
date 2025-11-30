from  django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.auth.views import CustomUserViewSet


router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix="",
    viewset=CustomUserViewSet,
    basename="user",
)

urlpatterns = [
    path("v1/", include(router.urls)),
]


