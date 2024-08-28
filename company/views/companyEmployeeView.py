from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

from company.forms.employeeForm import EmployeeForm
from company.models import CompanyEmployee, Unit, Department, Title
from icparsa.decorators import allowed_users


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def saveEmployee(request):
    next_number = CompanyEmployee.objects.all().count() + 1
    employeeForm = EmployeeForm(initial={'number': next_number})
    if request.method == 'POST':
        employeeForm = EmployeeForm(request.POST)
        employeeForm.save()
        return redirect('cem')
    context = {'employeeForm': employeeForm}
    return render(request, 'company/employee/employee.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def listEmployee(request):
    employeeList = CompanyEmployee.objects.all()
    context = {'employeeList': employeeList}
    return render(request, 'company/employee/listEmployee.html', context)


def updateEmployee(request, pk):
    emp = CompanyEmployee.objects.get(id=pk)
    empForm = EmployeeForm(instance=emp)
    if request.method == 'POST':
        empForm = EmployeeForm(request.POST, instance=emp)
        if empForm.is_valid():
            empForm.save()
            return redirect('lem')
    context = {'employeeForm': empForm}
    return render(request, 'company/employee/employee.html', context)


def recordSystemUserAsEmployee(request, pk):
    syst_user = get_object_or_404(User, id=pk)
    employee = CompanyEmployee()
    next_number = CompanyEmployee.objects.all().count() + 1
    for field in syst_user._meta.fields:
        if field.name in [f.name for f in employee._meta.fields]:
            setattr(employee, field.name, getattr(syst_user, field.name))
    employee.first_name = syst_user.first_name
    employee.last_name = syst_user.last_name

    if request.method == 'POST':
        empForm = EmployeeForm(request.POST, instance=employee)
        if empForm.is_valid():
            empForm.save()
            # return redirect('syem', pk=employee.pk)
            return redirect('home')

    else:
        empForm = EmployeeForm(initial={'number': next_number}, instance=employee)

    context = {'employeeForm': empForm}
    return render(request, 'company/employee/employee.html', context)


def loadTitle(request):
    department_id = request.GET.get('department_id')
    title = Title.objects.filter(department_id=department_id).order_by('name')
    context = {'title': title}
    return render(request, 'company/title/titleDropDown.html', context)


def load_unit(request):
    department_id = request.GET.get('department_id')
    unit = Unit.objects.filter(department_id=department_id)
    context = {'unit': unit}
    return render(request, 'company/unit/unitDropDown.html', context)


def loadDepartment(request):
    company_id = request.GET.get('company_id')
    department = Department.objects.filter(company_id=company_id)
    context = {'department': department}
    return render(request, 'company/department/departmentDropDown.html', context)
