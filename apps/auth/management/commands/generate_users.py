from random import randint, choice
from faker import Faker
from typing import Any

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from apps.auth.models import CustomUser


class Command(BaseCommand):
    help = "Generate 10000 random users for testing purposes"

    def handle(self, *args: Any, **kwargs: dict[str, Any]):
        fake = Faker()

        departments: list[str] = [
            dept[0] for dept in CustomUser.DEPARTMENT_CHOICES
        ]
        roles: list[str] = [
            role[0] for role in CustomUser.ROLES_CHOICES
        ]

        password = make_password("qwerty5")

        users: list["CustomUser"] = []
        for _ in range(10000):
            first_name: str = fake.first_name()
            last_name: str = fake.last_name()
            username: str = (
                f"{first_name.lower()}.{last_name.lower()}{randint(1, 9999)}"
            )
            email: str = f"{username}@{fake.free_email_domain()}"
            phone: str = fake.phone_number()
            department: str = choice(departments)
            role: str = choice(roles)
            birth_date = fake.date_of_birth(
                minimum_age=19,
                maximum_age=50,
            )

            new_user: "CustomUser" = CustomUser(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                department=department,
                role=role,
                birth_date=birth_date,
                password=make_password(password),
            )

            users.append(new_user)

        CustomUser.objects.bulk_create(users)
        print("Successfully created 10000 users.")
