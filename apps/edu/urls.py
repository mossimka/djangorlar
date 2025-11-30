from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.edu.views import CourseViewSet, LessonViewSet


router: DefaultRouter = DefaultRouter(trailing_slash=False)
router.register(prefix="courses", viewset=CourseViewSet, basename="courses")
router.register(prefix="lessons", viewset=LessonViewSet, basename="lessons")

urlpatterns = [
    path("v1/", include(router.urls)),
]
