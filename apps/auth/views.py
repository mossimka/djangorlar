from typing import Any

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from apps.auth.serializers import UserLoginSerializer
from apps.auth.models import CustomUser

"""
1.1. Description: Obtain access & refresh tokens Method: POST Path: /api/token. Permissions: Public. Request body: username and password Response body: refresh, access

1.2. Description: Refresh access token Method: POST Path: /api/token/refresh/ Permissions: Public Request body: refresh Response body: refresh
"""


class CustomUserViewSet(ViewSet):
    """
    View set for managing CustomUser instances.
    """
    permission_classes = (AllowAny,)


        methods=["post",],
        detail=True,
        permission_classes=[AllowAny],
        url_name="login",
        url_path="token",
    )
    def login(self, request: Request, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        """
        implementation of user login
        Args:
            request (Request): The incoming request object.
        Returns:
            Response: A response indicating the result of the login attempt.
        """

        serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: CustomUser = serializer.validated_data["user"]


        refresh: RefreshToken = RefreshToken.for_user(user)
        access: AccessToken = refresh.access_token

        return Response(
            data={
                "refresh": str(refresh),
                "access": str(access),
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "detail": "Login successful!",
            },
            status=HTTP_200_OK,
        )
    
    @action(
        methods=["post",],
        detail=True,
        permission_classes=[AllowAny],
        url_name="token_refresh",
        url_path="token/refresh",
    )
    def refresh_token(self, request: Request, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        """
        Fetcting refresh token
        
        Args:
            request (Request): The incoming request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.
        Returns:
            Response: A response containing the new access token.
        """

        refresh_token = request.data.get("refresh", None)

        if not refresh_token:
            return Response(
                data={
                    "detail": "Refresh token is required."
                },
                status=HTTP_400_BAD_REQUEST,
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            return Response(
                data={
                    "access": str(access),
                    "detail": "Access token refreshed successfully!",
                },
                status=HTTP_200_OK,
            )
        except Exception:
            return Response(
                data={
                    "detail": "Invalid refresh token."
                },
                status=HTTP_400_BAD_REQUEST,
            )

    @action(
        methods=["get",],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_name="user_info",
        url_path="user_info",
    )
    def fetch_user_info(self, request: Request, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        """
        Fetches information of an authenticated user
        Args:
            request (Request): The incoming request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.
        Returns:
            Response: A response containing the user's information.
        """

        user: CustomUser = request.user

        return Response(
            data = {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "detail": "User information fetched successfully!",
            },
            status=HTTP_200_OK,
        )