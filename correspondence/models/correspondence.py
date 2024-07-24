from django.db import models

from company.models import Department, Unit


class Correspondence(models.Model):
    TYPE = (
        ('INCOMING', 'INCOMING'),
        ('OUTGOING', 'GOING'))

    number = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateField(null=True, blank=True)
    organisation = models.CharField(max_length=100, null=True, blank=True)
    subject = models.TextField(max_length=250, null=True, blank=True)
    reference_number = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(Unit, max_length=100, null=True, blank=True, on_delete=models.ForeignKey)
    responsible = models.CharField(max_length=150, null=True, blank=True)
    correspondence_type = models.CharField(choices=TYPE, null=True, blank=True, max_length=250)

    def __str__(self):
        return self.organisation
