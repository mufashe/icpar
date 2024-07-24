from django.db import models

from company.models import Company, Department


class Unit(models.Model):
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=150, null=True, blank=True)
    company = models.ForeignKey(Company, max_length=150, null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, max_length=150, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
