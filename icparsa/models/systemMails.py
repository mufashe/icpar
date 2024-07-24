from django.db import models


class SystemMail(models.Model):
    number = models.IntegerField(null=True, blank=True)
