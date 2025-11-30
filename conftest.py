import pytest

from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

User = get_user_model()


# --------------------------------------------------------------
# General Fixtures


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        first_name="Test",
        last_name="Testovich",
        password="12345",
    )


@pytest.fixture
def spy_user(db):
    return User.objects.create_user(
        username="spyuser",
        email="spyuser@example.com",
        first_name="Spy",
        last_name="User",
        password="54321",
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def spy_auth_client(api_client, spy_user):
    api_client.force_authenticate(user=spy_user)
    return api_client


# --------------------------------------------------------------
# Course fixtures


@pytest.fixture
def course(user):
    from apps.edu.models import Course

    return Course.objects.create(
        title="Django Course",
        description="Learn Django from scratch",
        owner=user,
    )


# --------------------------------------------------------------
# Lesson fixtures


@pytest.fixture
def lesson(course):
    from apps.edu.models import Lesson

    return Lesson.objects.create(
        title="Introduction to Django",
        content="This is the first lesson.",
        course=course,
        order=1,
        indentation=0,
        is_published=True,
    )


# --------------------------------------------------------------
# Token fixtures


@pytest.fixture
def tokens(auth_client, user):
    response = auth_client.post(
        "/api/auth/v1/token",
        data={"email": user.email, "password": "12345"},
    )
    return {
        "access": response.data["access"],
        "refresh": response.data["refresh"],
    }
