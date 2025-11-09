from datetime import timedelta, date

from django.utils.timezone import now
from django.db.models import (
    Q,
    Count,
    Avg,
    Min,
    Max,
    Sum,
    Value,
    WHEN,
    CASE,
    CharField,
    ExpressionWrapper,
    F,
    DurationField,
)
from django.db.models.functions import (
    Concat,
    ExtractYear,
    Now,
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
CustomUser.objects.aggregate(Avg_salary=Avg("salary"))

# 2.22
CustomUser.objects.aggregate(Max_salary=Max("salary"), Min_salary=Min("salary"))

# 2.23
CustomUser.objects.filter(phone__contains="+7")

# 2.24
CustomUser.objects.annotate(full_name=Concat("first_name", Value(" "), "last_name"))

# 2.25
CustomUser.objects.annotate(birth_year=ExtractYear("birth_date")).order_by("birth_year")

# 2.26
CustomUser.objects.filter(birth_date__month=5)

# 2.27
CustomUser.objects.filter(role="Manager", salary_gt=400_000)

# 2.28
CustomUser.objects.filter(Q(role="Employee") | Q(department="HR"))

# 2.29
CustomUser.objects.filter(is_active=True).values("city").annotate(total=Count("id"))

# 2.30
CustomUser.objects.order_by("date_joined")[:10]

# 2.31
CustomUser.objects.filter(city__istartwith="A", salary_gt=300_000)

# 2.32
CustomUser.objects.filter(Q(department__isnull=True) | Q(department=""))

# 2.33
CustomUser.objects.values("country").annotate(total=Count("id"), Avg=Avg("salary"))

# 2.34
CustomUser.objects.filter(is_staff=True).order_by("-last_login")

# 2.35
CustomUser.objects.exclude(email__icontains="examle.com")

# 2.36
Avg_salary = CustomUser.objects.aggregate(Avg=Avg("salary"))["Avg"]
CustomUser.objects.filter(salary__gt=Avg_salary)

# 2.37
CustomUser.objects.values("email").annotate(total=Count("id")).filter(total__gt=1)

# 2.38
CustomUser.objects.annotate(
    salary_level=CASE(
        WHEN(salary__lt=300_000, then=Value("low")),
        WHEN(salary__lt=700_000, then=Value("medium")),
        default=Value("high"),
        output_field=CharField(),
    )
)

# 2.39
cur_year = date.today().year
CustomUser.objects.filter(date_joined__year=cur_year)

# 2.40
CustomUser.objects.values("department").annotate(total_payroll=Sum("Salary"))

# 2.41
CustomUser.objects.filter(department="IT", last_login__isnull=True)

# 2.42
CustomUser.objects.filter(country="Kazakhstan").filter(
    Q(city__isnull=True) | Q(city="")
)

# 2.43
CustomUser.objects.filter(birth_date__lt="1990-01-01", salary__isnull=False)

# 2.44
CustomUser.objects.annotate(
    years_since_joined=ExpressionWrapper(
        Now() - F("date_joined"), output_field=DurationField
    )
)

# 2.45
CustomUser.objects.filter(
    department="Sales",
    email_iendswith="@gmail.com",
    salary_gt=300_000,
)

# 2.46
CustomUser.objects.order_by("country", "-salary")

# 2.47
CustomUser.objects.values("role").annotate(total=Count("id")).filter(total_gt=100)

# 2.48
CustomUser.objects.filter(last_login__lt=F("date_joined"))

# 2.49
CustomUser.objects.annotate(
    is_senoir=CASE(
        WHEN(birth_date__lt="1985-01-01", then=Value(True)), default=Value(False)
    )
)

# 2.50
CustomUser.objects.values("department").annotate(
    total=Count("id"), avg_salary=Avg("salary")
).filter(total__gte=20).order_by("-avg_salary")