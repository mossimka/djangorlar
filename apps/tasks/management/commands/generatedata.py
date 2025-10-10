from typing import Any
from random import choice, choices
from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet

from apps.tasks.models import Project, Task, UserTask


class Command(BaseCommand):

    EMAIL_DOMAINS = [
        'example.com',
        'test.com',
        'sample.org',
        'demo.net',
        'mail.com',
        'aboba.fun',
    ]

    FIRST_NAMES = [
        'John', 'Jane', 'Alice', 
        'Bob', 'Charlie', 'Frances',
        'Eve', 'Frank', 'Grace',
    ]

    LAST_NAMES = [
        'Smith', 'Doe', 'Johnson',
        'Brown', 'Davis', 'Miller',
        'Wilson', 'Moore', 'Taylor',
    ]

    WORDS = [
        'lorem', 'ipsum', 'dolor',
        'sit', 'amet', 'consectetur',
        'adipiscing', 'elit', 'sed',
        'do', 'eiusmod', 'tempor',
        'incididunt', 'ut', 'labore',
        'et', 'dolore', 'magna',
    ]


    def __generate_users(self, count: int = 100) -> None:
        """
        Generate random users and save them to the database.
        """
        created_users: list[User] = []
        USER_PASSWORD = make_password('password123')
        users_before = User.objects.count()

        for i in range(count):
            username = f'user.{i}'
            email = f'{username}@{choice(self.EMAIL_DOMAINS)}'
            first_name = choice(self.FIRST_NAMES)
            last_name = choice(self.LAST_NAMES)
            created_users.append(
                User(
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    password = USER_PASSWORD,
                )
            )

        User.objects.bulk_create(created_users)
        users_after = User.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {users_after - users_before} users.'
            )
        )


    def __generate_projects(self, count: int = 25) -> None:
        """
        Generate random projects and save them to the database.
        """
        created_projects: list[Project] = []
        users: QuerySet[User] = User.objects.all()
        projects_before = Project.objects.count()

        for i in range(count):
            author = choice(users)
            name = ' '.join(choices(self.WORDS, k = 3)) + choice(users).username

            created_projects.append( 
                Project(
                    name = name,
                    author = author,
                )
            )

        Project.objects.bulk_create(created_projects)
        projects_after = Project.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {projects_after - projects_before} projects.'
            )
        )

    
    def handle(self, *args, **options):
        """
        Command entry point.
        """

        start_time = datetime.now()
        self.__generate_users()
        self.__generate_projects()

        self.stdout.write(
            self.style.SUCCESS(
                f'Data generation completed in {(datetime.now() - start_time).total_seconds()} seconds.'
            )
        )
