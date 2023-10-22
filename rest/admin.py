from django.contrib import admin
from django.db.models.functions import Concat
from django.db.models import Value, QuerySet
from .models import Employee, Department


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "department")
    list_select_related = ("department",)
    list_filter = ("department", )
    search_fields = ("first_name", "last_name", "middle_name", "position", "department__name")

    def full_name(self, instance: Employee) -> str:
        return instance.full_name

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        qs = super().get_queryset(*args, **kwargs)
        return qs.annotate(full_name=Concat('first_name', Value(' '), 'last_name', Value(' '), 'middle_name'))


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent")
    list_select_related = ("parent",)
    list_filter = ("parent",)
    search_fields = ("name",)

    def parent(self, instance: Department) -> str:
        return instance.parent.name
