from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from icparsa.decorators import allowed_users
from icparsa.forms.DepartmentMemberForm import DepartmentMemberForm
from icparsa.models import DepartmentMember, ContractSettingName


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='log')
def createDepartmentMember(request):
    nexNumber = DepartmentMember.objects.all().count() + 1
    departmentMemberForm = DepartmentMemberForm(initial={'number': nexNumber})
    if request.method == 'POST':
        departmentMemberForm = DepartmentMemberForm(request.POST)
        departmentMemberForm.save()
        return redirect('dem')
    context = {'departmentMemberForm': departmentMemberForm}
    return render(request, 'icparsa/settings/system/departmentMember.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='log')
def updateDepartmentMember(request, pk):
    unit = DepartmentMember.objects.get(id=pk)
    departmentMemberForm = DepartmentMemberForm(instance=unit)

    if request.method == 'POST':
        departmentMemberForm = DepartmentMemberForm(request.POST, instance=unit)
        if departmentMemberForm.is_valid():
            departmentMemberForm.save()
            return redirect('ldem')
    context = {'departmentMemberForm': departmentMemberForm, 'unit': unit}
    return render(request, 'icparsa/settings/system/departmentMember.html', context)


@login_required(login_url='log')
def listDepartmentMember(request):
    membersList = DepartmentMember.objects.all()
    context = {'membersList': membersList}
    return render(request, 'icparsa/settings/system/listMembers.html', context)


@login_required(login_url='log')
def load_department_members(request):
    department_id = request.GET.get('department_id')
    units = DepartmentMember.objects.filter(department_id=department_id)
    context = {'units': units}
    return render(request, 'icparsa/settings/system/member_drop.html', context)



