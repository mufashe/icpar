from django.contrib import admin

# Register your models here.

from .models import Contract, SecondParty
from .models.models import *
from .models.secondPartyType import SecondPartyType
from .models.departmentMemberModel import DepartmentMember
from .models.departmentModel import Department

admin.site.register(Contract),
admin.site.register(SecondParty),
admin.site.register(SecondPartyType),
admin.site.register(Department),
admin.site.register(DepartmentMember),
admin.site.register(ContractSetting),
