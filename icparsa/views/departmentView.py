from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from icparsa.decorators import allowed_users
from icparsa.forms.DepartmentForm import DepartmentForm
from icparsa.models import Department


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='log')
def createDepartment(request):
    nextNumber = Department.objects.all().count() + 1
    departmentForm = DepartmentForm(initial={'number': nextNumber})
    if request.method == 'POST':
        departmentForm = DepartmentForm(request.POST)
        departmentForm.save()
        return redirect('dem')
    context = {'departmentForm': departmentForm}
    return render(request, 'icparsa/settings/system/department.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='log')
def listDepartment(request):
    departmentList = Department.objects.all()
    context = {'departmentList': departmentList}
    return render(request, 'icparsa/settings/system/listDepartment.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='log')
def updateDepartment(request, pk):
    dep = Department.objects.get(id=pk)
    departmentForm = DepartmentForm(instance=dep)
    if request.method == 'POST':
        departmentForm = DepartmentForm(request.POST, instance=dep)
        if departmentForm.is_valid():
            departmentForm.save()
            return redirect('dep')

    context = {'departmentForm': departmentForm, 'dep': dep}
    return render(request, 'icparsa/settings/system/department.html', context)
