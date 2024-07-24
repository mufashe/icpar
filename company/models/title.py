from django.db import models

from .unit import Unit
from .company import Company
from .department import Department


class Title(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=150, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
