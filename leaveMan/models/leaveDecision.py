from django.contrib.auth.models import User
from django.db import models

from company.models import CompanyEmployee, EmployeeAsUserSignature
from leaveMan.models import Leave


class LeaveDecision(models.Model):
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE)
    requestingEmployee = models.ForeignKey(CompanyEmployee, related_name='requested_leaves', on_delete=models.CASCADE)
    approvingEmployee = models.ForeignKey(User, related_name='approved_leaves', on_delete=models.CASCADE)
    decisionStatus = models.CharField(max_length=100, null=True, blank=True, default='Pending')
    signature = models.ForeignKey(EmployeeAsUserSignature, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Decision for leave of {self.leave.employee.first_name} ({self.decisionStatus})"

