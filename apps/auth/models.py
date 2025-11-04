from django.db.models import (
    Model,
    CharField,
    EmailField,
    DateTimeField,
    IntegerField,
    ForeignKey,
    CASCADE,
    Choices,
    BooleanField,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from apps.abstract.models import AbstractBaseModel
from apps.auth.validators import phone_validator


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    Customer user model extending AbstractBaseUser and AbstractBaseModel.
    """

    EMAIL_FIELD_MAX_LENGTH: int = 255
    USERNAME_FIELD_MAX_LENGTH: int = 50
    NAME_FIELD_MAX_LENGTH: int = 30
    CITY_FIELD_MAX_LENGTH: int = 50
    COUNTRY_FIELD_MAX_LENGTH: int = 50

    DEPARTMENT_CHOICES: dict[str, str] = Choices(
        ("HR", "Human Resources"),
        ("IT", "Information Technology"),
        ("Finance", "Finance"),
        ("Marketing", "Marketing"),
    )
    ROLES_CHOICES: dict[str, str] = Choices(
        ("Admin", "Administrator"),
        ("User", "Standard User"),
        ("Manager", "Manager"),
        ("Guest", "Guest User"),
    )

    email = EmailField(unique=True, max_length=EMAIL_FIELD_MAX_LENGTH)
    username = CharField(max_length=USERNAME_FIELD_MAX_LENGTH, unique=True)
    first_name = CharField(max_length=NAME_FIELD_MAX_LENGTH, blank=True)
    last_name = CharField(max_length=NAME_FIELD_MAX_LENGTH, blank=True)
    phone = CharField(max_length=15, blank=True, validators=[phone_validator])
    city = CharField(max_length=CITY_FIELD_MAX_LENGTH, blank=True)
    country = CharField(max_length=COUNTRY_FIELD_MAX_LENGTH, blank=True)
    department = CharField(max_length=30, blank=True, choices=DEPARTMENT_CHOICES)
    role = CharField(max_length=30, blank=True, choices=ROLES_CHOICES)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    date_joined = DateTimeField(auto_now_add=True)
    last_login = DateTimeField(null=True, blank=True)
    