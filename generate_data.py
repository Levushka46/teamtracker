import random
import sqlite3
import os
import django
import pytz
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamtracker.settings")
django.setup()

from django.db import transaction
from django.db.utils import IntegrityError
from rest.models import Employee, Department
from teamtracker import settings
from math import floor

fake = Faker()


def create_employees(num_employees):
    print("Employee creation started")
    department_objects = list(Department.objects.all())
    employees = []
    for _ in range(num_employees):
        first_name = fake.first_name()
        last_name = fake.last_name()
        middle_name = fake.first_name()
        position = fake.job()
        employment_date = fake.date_time_this_decade().replace(tzinfo=pytz.UTC)
        salary = round(random.normalvariate(50000, 10000), 2)
        department = random.choice(department_objects)

        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            position=position,
            employment_date=employment_date,
            salary=salary,
            department=department,
        )
        employees.append(employee)

    Employee.objects.bulk_create(employees)


def create_department_hierarchy():
    print("Department creation started")
    heads = [
        "Администрация",
        "Финансы",
        "Разработка",
        "Бухгалтерия",
        "Инвестиции",
        "Разработка ПО",
        "Контроль качества",
    ]
    heads.extend([f"Подразделение {ch}" for ch in range(1, 9)])
    heads.extend([f"Отделение {ch}" for ch in range(1, 11)])

    deps = []
    for i in range(1, len(heads) + 1):
        if i - 1 != 0:
            parent = deps[floor(i / 2) - 1]
        else:
            parent = None
        name = heads[i - 1]
        deps.append(Department.objects.create(name=name, parent=parent))


def main():
    if Department.objects.all().count() == 0:
        with transaction.atomic():
            create_department_hierarchy()
        create_employees(50000)
    else:
        print("Database is already full")


if __name__ == "__main__":
    main()
