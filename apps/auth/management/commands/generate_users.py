from random import randint, choice
from faker import Faker
from typing import Any

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from apps.auth.models import CustomUser


class Command(BaseCommand):
    help = "Generate 10,000 random users for testing purposes"

    def handle(self, *args: Any, **kwargs: dict[str, Any]):
        fake = Faker()

        departments = [dept[0] for dept in CustomUser.DEPARTMENT_CHOICES]
        roles = [role[0] for role in CustomUser.ROLES_CHOICES]

        BATCH_SIZE = 1000
        TOTAL = 10000
        password_hash = make_password("qwerty5")

        users = []
        created = 0

        for i in range(TOTAL):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}{randint(1, 9999)}"
            email = f"{username}@{fake.free_email_domain()}"
            phone = fake.phone_number()
            department = choice(departments)
            role = choice(roles)
            birth_date = fake.date_of_birth(minimum_age=19, maximum_age=50)

            users.append(
                CustomUser(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    department=department,
                    role=role,
                    birth_date=birth_date,
                    password=password_hash,
                )
            )

            if len(users) >= BATCH_SIZE:
                CustomUser.objects.bulk_create(users)
                created += len(users)
                self.stdout.write(f"Inserted {created}/{TOTAL} users...")
                users.clear()

        # create the remaining users
        if users:
            CustomUser.objects.bulk_create(users)
            created += len(users)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {created} users."))
