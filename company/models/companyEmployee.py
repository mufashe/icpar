from django.db import models

from company.models import Title, Department


class CompanyEmployee(models.Model):
    number = models.IntegerField(null=True, blank=True)
    emp_code = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    home_phone = models.IntegerField(null=True, blank=True)
    mobile_phone = models.IntegerField(null=True, blank=True)
    home_address = models.CharField(max_length=150, null=True, blank=True)

    hire_date = models.DateField(null=True, blank=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)

    # months_in_institution = models.IntegerField(null=True, blank=True)
    # total_leave_days = models.IntegerField(null=True, blank=True)
    # leave_days_used = models.IntegerField(null=True, blank=True)
