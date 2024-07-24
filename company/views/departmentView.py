from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from company.forms.departmentForm import DepartmentForm
from company.models.department import Department
from icparsa.decorators import allowed_users


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def createDepartment(request):
    next_number = Department.objects.all().count() + 1
    departmentForm = DepartmentForm(initial={'number': next_number})
    if request.method == 'POST':
        departmentForm = DepartmentForm(request.POST)
        departmentForm.save()
        return redirect('ld')
    context = {'departmentForm': departmentForm}
    return render(request, 'company/department.html', context)


@login_required(login_url='log')
def listDepartment(request):
    departmentList = Department.objects.all()
    context = {'listDepartment': departmentList}
    return render(request, 'company/listDepartment.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def updateDepartment(request, pk):
    department = Department.objects.get(id=pk)
    departmentForm = DepartmentForm(instance=department)
    if request.method == 'POST':
        departmentForm = DepartmentForm(request.POST, instance=department)
        if departmentForm.is_valid():
            departmentForm.save()
            return redirect('ld')

    context = {'departmentForm': departmentForm, 'department': department}
    return render(request, 'company/department.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def deleteDepartment(request, pk):
    department = Department.objects.get(id=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('ld')
    context = {'department': department}
    return render(request, 'company/deleteDepartment.html', context)
