from conftest import spy_auth_client, auth_client, course, api_client, lesson

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)
from rest_framework.response import Response


# create
def test_create_lesson(auth_client, course):
    data = {
        "title": "New Lesson",
        "content": "This is the content of the new lesson.",
        "course": course.id,
        "indentation": 0,
        "is_published": True,
    }
    response: Response = auth_client.post("/api/edu/v1/lessons", data)

    assert response.status_code == HTTP_201_CREATED
    assert response.data["title"] == data["title"]


def test_create_lesson_not_owner(spy_auth_client, course):
    data = {
        "title": "Spy Lesson",
        "content": "This is the content of the spy lesson.",
        "course": course.id,
        "indentation": 0,
        "is_published": True,
    }
    response: Response = spy_auth_client.post("/api/edu/v1/lessons", data)

    assert response.status_code == HTTP_403_FORBIDDEN


# move
def test_move_lesson(auth_client, course, lesson):
    res: Response = auth_client.post(
        f"/api/edu/v1/lessons/{lesson.id}/move", {"new_course_id": course.id}
    )
    assert res.status_code == HTTP_200_OK


# delete
def test_delete_lesson(auth_client, lesson):
    response: Response = auth_client.delete(f"/api/edu/v1/lessons/{lesson.id}")
    assert response.status_code == HTTP_200_OK


def test_delete_lesson_not_owner(spy_auth_client, lesson):
    response: Response = spy_auth_client.delete(f"/api/edu/v1/lessons/{lesson.id}")
    assert response.status_code == HTTP_403_FORBIDDEN


# publish/unpublish
def test_publish_lesson(auth_client, lesson):
    response: Response = auth_client.post(f"/api/edu/v1/lessons/{lesson.id}/publish")
    assert response.status_code == HTTP_200_OK


def test_unpublish_lesson(auth_client, lesson):
    response: Response = auth_client.post(f"/api/edu/v1/lessons/{lesson.id}/unpublish")
    assert response.status_code == HTTP_200_OK


def test_publish_lesson_not_owner(spy_auth_client, lesson):
    response: Response = spy_auth_client.post(
        f"/api/edu/v1/lessons/{lesson.id}/publish"
    )
    assert response.status_code == HTTP_403_FORBIDDEN
