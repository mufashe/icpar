from django.db import models


class Department(models.Model):
    number = models.IntegerField(null=True)
    name = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
