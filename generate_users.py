import random
import sqlite3
import os
import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamtracker.settings")
django.setup()

from django.db import transaction
from django.db.utils import IntegrityError
from rest.models import Employee, Department
from teamtracker import settings

fake = Faker()

department_objects = list(Department.objects.all())

def create_employees(num_employees):
    employees = []
    for _ in range(num_employees):
        first_name = fake.first_name()
        last_name = fake.last_name()
        middle_name = fake.first_name()
        position = fake.job()
        employment_date = fake.date_time_this_decade()
        salary = round(
            random.normalvariate(50000, 10000), 2
        )
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


def create_department_hierarchy(name, parent=None, depth=1, max_depth=5, max_children=5):
    if depth > max_depth:
        return

    department = Department.objects.create(name=name, parent=parent)

    num_children = random.randint(0, max_children)
    for _ in range(num_children):
        child_name = f"{name} Subdepartment {depth}-{_ + 1}"
        create_department_hierarchy(child_name, parent=department, depth=depth + 1, max_depth=max_depth, max_children=max_children)

# Начинаем создание иерархии
with transaction.atomic():
    create_department_hierarchy("Department", max_depth=5, max_children=5)

# Создаем 50000 записей Employee
create_employees(50000)
