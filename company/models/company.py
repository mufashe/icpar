from django.db import models


class Company(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
