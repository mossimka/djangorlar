from conftest import spy_auth_client, auth_client, user

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.response import Response


def test_get_token(api_client, user):
    response = api_client.post(
        "/api/auth/v1/token",
        data={"email": user.email, "password": "12345"},
    )
    assert response.status_code == HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


def test_get_token_invalid_credentials(api_client, user):
    response = api_client.post(
        "/api/auth/v1/token",
        data={"email": user.email, "password": "invalid_password"},
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_refresh_token(auth_client, tokens):
    response: Response = auth_client.post(
        "/api/auth/v1/token/refresh", data={"refresh": tokens["refresh"]}
    )
    assert response.status_code == HTTP_200_OK
    assert "access" in response.data


def test_refresh_token_invalid_token(auth_client):
    response: Response = auth_client.post(
        "/api/auth/v1/token/refresh", data={"refresh": "invalid_token"}
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "access" not in response.data
