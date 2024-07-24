from django.db import models


class SecondPartyType(models.Model):
    number = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
