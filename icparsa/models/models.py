from django.db import models

# Create your models here.
from icparsa.models.secondPartyType import SecondPartyType
from .contractSetting import ContractSetting, ContractSettingName
from .departmentMemberModel import DepartmentMember
from .departmentModel import Department


class SecondParty(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    number = models.IntegerField(null=True)
    name = models.CharField(max_length=250, null=True)
    spType = models.ForeignKey(SecondPartyType, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Contract(models.Model):
    # Contract_Type = (
    #     ('Framework', 'Framework contract'),
    #     ('Determined', 'Others'))

    STATUS = (

        ('SIGNED', 'SIGNED'),
        ('CANCELED', 'CANCELED')
    )

    date_created = models.DateField(auto_now_add=True, null=True)
    number = models.IntegerField(null=True)
    name = models.CharField(null=True, max_length=200)
    contractCategory = models.ForeignKey(ContractSettingName, on_delete=models.SET_NULL, null=True, blank=True)
    contractType = models.ForeignKey(ContractSetting, on_delete=models.SET_NULL, null=True, blank=True)
    contract_status = models.CharField(choices=STATUS, max_length=100, default='SIGNED')
    secondParty = models.ForeignKey(SecondParty, on_delete=models.SET_NULL, null=True, blank=True)
    signedDate = models.DateField(blank=True, null=True)
    expirationDate = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, max_length=250, null=True)
    departmentUnit = models.ForeignKey(DepartmentMember, on_delete=models.SET_NULL, null=True, blank=True)
    notificationSent = models.BooleanField(default=False)
    notificationSentOn = models.DateField(blank=True, null=True)
    notificationRemindingTimes = models.IntegerField(blank=True, null=True, default=0)
    notificationWaitingInterval = models.IntegerField(blank=True, null=True)
    renewed = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class ContractHistory(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    signedDate = models.DateField(blank=True, null=True)
    expirationDate = models.DateField(blank=True, null=True)
    renewDate = models.DateField(blank=True, null=True)
    renewalCounter = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.contract.name} History'
