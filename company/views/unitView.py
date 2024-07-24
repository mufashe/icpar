from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from company.forms.unitForm import UnitForm
from company.models import Unit
from icparsa.decorators import allowed_users


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def createUnit(request):
    next_number = Unit.objects.all().count() + 1
    unitForm = UnitForm(initial={'number': next_number})
    if request.method == 'POST':
        unitForm = UnitForm(request.POST)
        unitForm.save()
        return redirect('lun')
    context = {'unitForm': unitForm}
    return render(request, 'company/unit.html', context)


@login_required(login_url='log')
def listUnit(request):
    unitList = Unit.objects.all()
    context = {'unitList': unitList}
    return render(request, 'company/listUnit.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def updateUnit(request, pk):
    unit = Unit.objects.get(id=pk)
    unitForm = UnitForm(instance=unit)
    if request.method == 'POST':
        unitForm = UnitForm(request.POST, instance=unit)
        if unitForm.is_valid():
            unit.save()
            return redirect('lun')

    context = {'unitForm': unitForm, 'unit': unit}
    return render(request, 'company/unit.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def deleteUnit(request, pk):
    unit = Unit.objects.get(id=pk)
    if request.method == 'POST':
        unit.delete()
        return redirect('/lun')
    context = {'unit': unit}
    return render(request, 'company/deleteUnit.html', context)
