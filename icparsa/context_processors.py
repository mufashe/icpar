from company.models import CompanyEmployee


def employeeProcessor(request):
    if request.user.is_authenticated:
        try:
            employee = CompanyEmployee.objects.get(email=request.user.email)
        except CompanyEmployee.DoesNotExist:
            employee = None
    else:
        employee = None
    return {'employee': employee}
