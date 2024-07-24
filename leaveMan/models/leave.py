from django.db import models

from company.models import Department, Title, CompanyEmployee


class Leave(models.Model):
    STATUS_OF_LEAVE = [
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('DENIED', 'DENIED'),
        ('DONE', 'DONE'),
    ]

    number = models.IntegerField(null=True, blank=True)
    employee = models.ForeignKey(CompanyEmployee, on_delete=models.CASCADE, null=True, blank=True)
    months_in_institution = models.IntegerField(null=True, blank=True)
    total_leave_days = models.IntegerField(null=True, blank=True)
    leave_days_used = models.IntegerField(null=True, blank=True, default=0)
    leave_days = models.IntegerField(null=True, blank=True, default=0)
    outDate = models.DateField(null=True, blank=True)
    inDate = models.DateField(null=True, blank=True)
    leave_status = models.CharField(max_length=100, choices=STATUS_OF_LEAVE, default='PENDING')
    approval_one = models.BinaryField(null=True, blank=True)

