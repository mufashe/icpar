from django.db import models

from .company import Company


class Department(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=150, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
