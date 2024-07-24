from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from company.models import Unit
from correspondence.forms.correspondenceForm import CorrespondenceForm
from correspondence.models import Correspondence
from icparsa.decorators import allowed_users


@allowed_users(allowed_roles=['admin', 'correspondence'])
@login_required(login_url='log')
def recordCorrespondence(request):
    next_number = Correspondence.objects.all().count() + 1
    corresForm = CorrespondenceForm(initial={'number': next_number})
    if request.method == 'POST':
        corresForm = CorrespondenceForm(request.POST)
        corresForm.save()
        return redirect('cor')
    context = {'corresForm': corresForm}
    return render(request, 'correspondence/correspondence.html', context)


@allowed_users(allowed_roles=['admin', 'correspondence'])
@login_required(login_url='log')
def listCorrespondence(request):
    correspondenceList = Correspondence.objects.all()
    context = {'correspondenceList': correspondenceList}
    return render(request, 'correspondence/listCorrespondence.html', context)


@allowed_users(allowed_roles=['admin', 'correspondence'])
@login_required(login_url='log')
def updateCorrespondence(request, pk):
    correspondence = Correspondence.objects.get(id=pk)
    correspondenceForm = CorrespondenceForm(instance=correspondence)
    if request.method == 'POST':
        correspondenceForm = CorrespondenceForm(request.POST, instance=correspondence)
        if correspondenceForm.is_valid():
            correspondence.save()
            return redirect('lic')
    context = {'corresForm': correspondenceForm, 'correspondence': correspondence}
    return render(request, 'correspondence/correspondence.html', context)


@allowed_users(allowed_roles=['admin', 'correspondence'])
@login_required(login_url='log')
def deleteCorrespondence(request, pk):
    correspondence = Correspondence.objects.get(id=pk)
    if request.method == 'POST':
        return redirect('/lic')
    context = {'correspondence': correspondence}
    return render(request, 'correspondence/deleteCorrespondence.html', context)


@allowed_users(allowed_roles=['admin', 'correspondence'])
@login_required(login_url='log')
def loadDepartmentUnit(request):
    department_id = request.GET.get('department_id')
    units = Unit.objects.filter(department_id=department_id)
    context = {'units': units}
    return render(request, 'correspondence/unitDrop.html', context)
