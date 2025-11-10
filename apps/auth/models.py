from typing import Any

from django.db.models import (
    CharField,
    EmailField,
    DateTimeField,
    BooleanField,
    IntegerField,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from apps.abstract.models import AbstractBaseModel
from apps.auth.validators import phone_validator


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for our custom user
    """

    def __obtain_user_instance(
        self,
        email: str,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        **kwargs: dict[str, Any]
    ) -> "CustomUser":
        if not email:
            raise ValueError(
                "The Email field is required", 
                code="email_empty",
            )
        if not username:
            raise ValueError(
                "The Username field is required", 
                code="username_empty",
            )
        if not password:
            raise ValueError(
                "The Password field is required", 
                code="password_empty",
            )
        if not first_name:
            raise ValueError(
                "The First Name field is required", 
                code="first_name_empty",
            )
        if not last_name:
            raise ValueError(
                "The Last Name field is required", 
                code="last_name_empty",
            )

        new_user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )

        return new_user
    
    def create_user(
        self,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> "CustomUser":
        new_user: "CustomUser" = self.__obtain_user_instance(
            email,
            username,
            first_name,
            last_name,
            password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save()
        return new_user
    
    def create_superuser(
        self,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, Any], 
    ) -> "CustomUser":
        new_user: "CustomUser" = self.__obtain_user_instance(
            email,
            username,
            first_name,
            last_name,
            password,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        new_user.set_password(password)
        new_user.save()
        return new_user



class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    Customer user model extending AbstractBaseUser and AbstractBaseModel.
    """

    EMAIL_FIELD_MAX_LENGTH: int = 255
    USERNAME_FIELD_MAX_LENGTH: int = 50
    NAME_FIELD_MAX_LENGTH: int = 30
    CITY_FIELD_MAX_LENGTH: int = 50
    COUNTRY_FIELD_MAX_LENGTH: int = 50

    DEPARTMENT_CHOICES: dict[str, str] = (
        ("HR", "Human Resources"),
        ("IT", "Information Technology"),
        ("Finance", "Finance"),
        ("Marketing", "Marketing"),
    )
    ROLES_CHOICES: dict[str, str] = (
        ("Admin", "Administrator"),
        ("User", "Standard User"),
        ("Manager", "Manager"),
        ("Guest", "Guest User"),
    )

    email = EmailField(unique=True, max_length=EMAIL_FIELD_MAX_LENGTH)
    username = CharField(max_length=USERNAME_FIELD_MAX_LENGTH, unique=True)
    first_name = CharField(max_length=NAME_FIELD_MAX_LENGTH, blank=True)
    last_name = CharField(max_length=NAME_FIELD_MAX_LENGTH, blank=True)
    salary = IntegerField(default=100_000)
    phone = CharField(max_length=15, blank=True, validators=[phone_validator])
    birth_date = DateTimeField(null=True, blank=True)
    city = CharField(max_length=CITY_FIELD_MAX_LENGTH, blank=True)
    country = CharField(max_length=COUNTRY_FIELD_MAX_LENGTH, blank=True)
    department = CharField(max_length=30, blank=True, choices=DEPARTMENT_CHOICES)
    role = CharField(max_length=30, blank=True, choices=ROLES_CHOICES)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    date_joined = DateTimeField(auto_now_add=True)
    last_login = DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ["-date_joined"]
