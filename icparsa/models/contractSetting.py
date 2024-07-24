from django.db import models


class ContractSettingName(models.Model):
    number = models.IntegerField(null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=250)

    def __str__(self):
        return self.name


class ContractSetting(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    expirationDays = models.IntegerField(null=True, blank=True)
    # type = models.CharField(max_length=150, null=True, blank=True)
    remindingTimes = models.IntegerField(null=True, blank=True, default=1)
    notificationsDaysToWait = models.IntegerField(blank=True, null=True)
    managingEmail = models.CharField(null=True, blank=True, max_length=250)
    renewTimes = models.IntegerField(null=True, blank=True, default=1)
    contractName = models.ForeignKey(ContractSettingName, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
