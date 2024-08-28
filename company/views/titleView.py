from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from company.forms.titleForm import TitleForm
from company.models import Unit, Department
from company.models.title import Title
from icparsa.decorators import allowed_users


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def createCompanyTitle(request):
    next_number = Title.objects.all().count() + 1
    titleForm = TitleForm(initial={'number': next_number})
    if request.method == 'POST':
        titleForm = TitleForm(request.POST)
        titleForm.save()
        return redirect('lt')
    context = {'titleForm': titleForm}
    return render(request, 'company/title.html', context)


@login_required(login_url='log')
def listTitle(request):
    titleList = Title.objects.all()

    context = {'titleList': titleList}
    return render(request, 'company/listTitle.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def updateTitle(request, pk):
    title = Title.objects.get(id=pk)
    titleForm = TitleForm(instance=title)
    if request.method == 'POST':
        titleForm = TitleForm(request.POST, instance=title)
        if titleForm.is_valid():
            titleForm.save()
            return redirect('lt')
    context = {'titleForm': titleForm, 'title': title}
    return render(request, 'company/title.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def deleteTitle(request, pk):
    title = Title.objects.get(id=pk)
    if request.method == 'POST':
        title.delete()
        return redirect('/lt')
    context = {'title': title}
    return render(request, 'company/deleteTitle.html', context)


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
