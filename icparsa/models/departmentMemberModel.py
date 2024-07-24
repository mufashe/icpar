from django.db import models

from .departmentModel import Department


class DepartmentMember(models.Model):
    number = models.IntegerField(null=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
