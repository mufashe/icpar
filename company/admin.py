from django.contrib import admin

# Register your models here.
from company.models import Umumaro, CompanyEmployee
from company.models.company import Company
from company.models.department import Department

from company.models.title import Title

admin.site.register(Company),
admin.site.register(Department),
admin.site.register(Title),
admin.site.register(Umumaro)
admin.site.register(CompanyEmployee)
