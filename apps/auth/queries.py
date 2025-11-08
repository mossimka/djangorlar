from datetime import timedelta, date

from django.utils.timezone import now
from django.db.models import (
    Q,
    Count,
    AVG,
    MIN,
    MAX,
    Value
)
from django.db.models.functions import (
    Concat,
    ExtractYear,
)

from apps.auth.models import CustomUser


# 2.1
CustomUser.objects.filter(is_active=True)

# 2.2
CustomUser.objects.filter(email__endswith="@gmail.com")

# 2.3
CustomUser.objects.filter(city__iexact="Almaty")

# 2.4
CustomUser.objects.exclude(city__iexact="Almaty")

# 2.5
CustomUser.objects.filter(salary__gt=500_000)

# 2.6
CustomUser.objects.filter(department="IT", country="Kazakhstan")

# 2.7
CustomUser.objects.filter(birth_date__isnull=True)

# 2.8
CustomUser.objects.filter(first_name__istartswith="A")

# 2.9
CustomUser.objects.count()

# 2.10
CustomUser.objects.order_by("-date_joined")[:20]

# 2.11
CustomUser.objects.values_list("city", flat=True).distinct()

# 2.12
CustomUser.objects.filter(department="Sales").count()

# 2.13
CustomUser.objects.filter(last_login__gte=now() - timedelta(days=7))

# 2.14
CustomUser.objects.filter(
    Q(first_name__icontains="bek") | Q(last_name__icontains="bek")
)

# 2.15
CustomUser.objects.filter(salary__rnage=(300_000, 700_000))

# 2.16
CustomUser.objects.filter(department__in=["IT", "HR", "Finance"])

# 2.17
CustomUser.objects.values("department").annotate(total=Count("id"))

# 2.18
CustomUser.objects.values("department").annotate(total=Count("id")).order_by("-total")

# 2.19
CustomUser.objects.values("city").annotate(total=Count("id")).order_by("-total")[:5]

# 2.20
CustomUser.objects.filter(last_login__isnull=True)

# 2.21
CustomUser.objects.aggregate(avg_salary=AVG("salary"))

# 2.22
CustomUser.objects.aggregate(max_salary=MAX("salary"), min_salary=MIN("salary"))

# 2.23
CustomUser.objects.filter(phone__contains="+7")

#2.24
CustomUser.objects.annotate(full_name=Concat("first_name", Value(" "), "last_name"))

#2.25
CustomUser.objects.annotate(birth_year=ExtractYear("birth_date")).order_by("birth_year")

"""
2.26 Get all users born in May (birth_date__month=5).

2.27 Get all users with role="manager" and salary greater than 400000.

2.28 Get all users with role="employee" or department "HR".

2.29 Count active users in each city (group by city, filter is_active=True).

2.30 Get the 10 earliest registered users (order by date_joined ascending).

2.31 Get users whose city starts with "A" and whose salary is greater than 300000.

2.32 Get all users with an empty or null department (check both isnull and empty string).

2.33 Get stats by country: country name, number of users, and average salary per country.

2.34 Get all staff users (is_staff=True) ordered by last_login descending.

2.35 Get all users whose email does not contain "example.com".

2.36 Get all users whose salary is higher than the average salary (two-step or subquery — your choice).

2.37 Find emails that are used by more than one user (group by email and filter by Count("id") > 1).

2.38 Annotate users with a computed field salary_level using Case/When: "low" for salary < 300000 "medium" for 300000–700000 "high" for > 700000 Then order by this annotated field.

2.39 Get all users whose date_joined is within the current year.

2.40 Get total payroll per department: for each department, sum of salary.

2.41 Get all users from "IT" department whose last_login is null — i.e. created but never logged in.

2.42 Get all users whose country="Kazakhstan" but city is null or empty — to find “incomplete” profiles.

2.43 Get all users whose birth_date is before 1990-01-01 and salary is not null.

2.44 Get all users and annotate them with years_since_joined (difference between today and date_joined in days/years — students can use ExpressionWrapper with Now()).

2.45 Get users whose department is "Sales" and whose email ends with @gmail.com and salary > 350000 (multiple filters).

2.46 Get all users, order them by country, and inside each country — by salary descending (multi-level ordering).

2.47 Get the number of users per role (group by role), but show only roles that have more than 100 users.

2.48 Get all users whose last_login is earlier than their date_joined (data inconsistency check).

2.49 Get all users and annotate them with is_senior = True if birth_date is before 1985-01-01, else False.

2.50 Create a query that returns departments sorted by average salary descending, but only for departments that have at least 20 users.
"""
