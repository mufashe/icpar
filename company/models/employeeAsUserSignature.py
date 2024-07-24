from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from jsignature.fields import JSignatureField

from company.models import CompanyEmployee


class EmployeeAsUserSignature(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    digital_signature = models.BinaryField(null=True, blank=True)
    signature_password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.signature_password = make_password(self.signature_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee.username

