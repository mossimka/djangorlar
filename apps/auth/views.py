from typing import Any

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from apps.auth.serializers import (
    UserLoginSerializer,
    RefreshTokenSerializer,
    UserInfoSerializer,
)
from apps.auth.models import CustomUser



class CustomUserViewSet(ViewSet):
    """
    View set for managing CustomUser instances.
    """

    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'refresh_token':
            return RefreshTokenSerializer
        if self.action == 'fetch_user_info':
            return UserInfoSerializer
        return None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if serializer_class:
            kwargs.setdefault('context', {'request': self.request, 'view': self})
            return serializer_class(*args, **kwargs)
        return None

    @action(
        methods=[
            "post",
        ],
        detail=False,
        permission_classes=[AllowAny],
        url_name="login",
        url_path="token",
    )
    def login(
        self, request: Request, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
        """
        Implementation of user login
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
        methods=[
            "post",
        ],
        detail=False,
        permission_classes=[AllowAny],
        url_name="token_refresh",
        url_path="token/refresh",
    )
    def refresh_token(
        self, request: Request, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
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
                data={"detail": "Refresh token is required."},
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
                data={"detail": "Invalid refresh token."},
                status=HTTP_400_BAD_REQUEST,
            )

    @action(
        methods=["get",],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_name="user_info",
        url_path="user_info",
    )
    def fetch_user_info(
        self, request: Request, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> Response:
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
            data={
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "detail": "User information fetched successfully!",
            },
            status=HTTP_200_OK,
        )
