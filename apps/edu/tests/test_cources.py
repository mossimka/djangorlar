from conftest import auth_client, user, course, api_client, spy_user, spy_auth_client

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)
from rest_framework.response import Response


# get
def test_list_courses(auth_client):
    response: Response = auth_client.get("/api/edu/v1/courses")
    assert response.status_code == HTTP_200_OK


def test_list_courses_unauthenticated(api_client):
    response: Response = api_client.get("/api/edu/v1/courses")
    assert response.status_code == HTTP_401_UNAUTHORIZED


# post
def test_create_course(auth_client):
    data = {
        "title": "New Course",
        "description": "This is a new course.",
    }
    response: Response = auth_client.post("/api/edu/v1/courses", data)

    assert response.status_code == HTTP_201_CREATED
    assert response.data["title"] == data["title"]


def test_create_course_invalid(auth_client):
    data = {
        "title": "",
        "description": "This is a new course.",
    }
    response: Response = auth_client.post("/api/edu/v1/courses", data)
    assert response.status_code == 400


# retrieve
def test_retrieve_course(auth_client, course):
    response: Response = auth_client.get(f"/api/edu/v1/courses/{course.id}")
    assert response.status_code == HTTP_200_OK


def test_retrieve_course_not_found(auth_client, course): # Changed api_client to auth_client
    response: Response = auth_client.get(f"/api/edu/v1/courses/9999")
    assert response.status_code == HTTP_404_NOT_FOUND


# update
def test_update_course(auth_client, course):
    data = {
        "title": "Updated Title",
        "description": "Updated Description",
    }
    response: Response = auth_client.put(f"/api/edu/v1/courses/{course.id}", data)
    assert response.status_code == HTTP_200_OK
    assert response.data["title"] == data["title"]
    assert response.data["description"] == data["description"]


def test_update_course_invalid(auth_client, course):
    data = {
        "title": "",
        "description": "Updated Description",
    }
    response: Response = auth_client.put(f"/api/edu/v1/courses/{course.id}", data)
    assert response.status_code == 400


def test_update_course_not_owner(spy_auth_client, course):
    data = {
        "title": "Updated Title",
        "description": "Updated Description",
    }
    response: Response = spy_auth_client.put(f"/api/edu/v1/courses/{course.id}", data)
    assert response.status_code == HTTP_403_FORBIDDEN # Changed 404 to 403


# delete
def test_delete_course(auth_client, course):
    response: Response = auth_client.delete(f"/api/edu/v1/courses/{course.id}")
    assert response.status_code == HTTP_200_OK


# activate/deactivate
def test_activate_course(auth_client, course):
    response: Response = auth_client.post(f"/api/edu/v1/courses/{course.id}/activate")
    assert response.status_code == HTTP_200_OK
    
    course.refresh_from_db()
    assert course.is_active is True


def test_deactivate_course(auth_client, course):
    response: Response = auth_client.post(f"/api/edu/v1/courses/{course.id}/deactivate")
    assert response.status_code == HTTP_200_OK
    
    course.refresh_from_db()
    assert course.is_active is False


def test_activate_course_not_owner(spy_auth_client, course):
    response: Response = spy_auth_client.post(
        f"/api/edu/v1/courses/{course.id}/activate"
    )
    assert response.status_code == HTTP_403_FORBIDDEN


# list lessons
def test_get_list_lessons(auth_client, course):
    response: Response = auth_client.get(f"/api/edu/v1/courses/{course.id}/lessons")
    assert response.status_code == HTTP_200_OK
