from django.db.models import Model, CharField, EmailField, BooleanField
from django.contrib.auth.models import AbstractUser, AbstractBaseUser,  PermissionsMixin


# Create your models here.
class CustomUser1(AbstractUser):
    phone = CharField(max_length=15, blank=True)
    address = CharField(max_length=255, blank=True)


class CustomUser2(AbstractBaseUser, PermissionsMixin):
    email = EmailField(unique=True)
    fullname = CharField(max_length=150, unique=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']