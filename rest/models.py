from django.db import models

from djmoney.money import Money
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    name = models.CharField(_("department name"), max_length=150, blank=True)
    parent = models.ForeignKey("self", verbose_name=_("parent department"), null=True, blank=True, on_delete=models.CASCADE, related_name="sub_departments")
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    middle_name = models.CharField(_("middle name"), max_length=150, blank=True)
    position = models.CharField(_("position"), max_length=75, blank=True)
    employment_date = models.DateTimeField(_("employment date"), auto_now_add=True)
    salary = MoneyField(_("salary"), default=Money("0.01", "RUB"), max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, verbose_name=_("department"), on_delete=models.CASCADE, related_name="department")

    def __str__(self):
        return self.first_name