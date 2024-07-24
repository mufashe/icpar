from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from icparsa.decorators import allowed_users
from icparsa.forms.InstitutionForm import InstitutionForm
from icparsa.models import SecondParty


@allowed_users(allowed_roles=['admin', 'procurement'])
@login_required(login_url='log')
def recordInstitute(request):
    nextNumber = SecondParty.objects.all().count() + 1
    institutionForm = InstitutionForm(initial={'number': nextNumber})
    if request.method == 'POST':
        institutionForm = InstitutionForm(request.POST)
        if institutionForm.is_valid():
            institutionForm.save()
            messages.success(request, 'Service Provider Created !')
            # return redirect('insts')
            institutionForm = InstitutionForm(initial={'number': nextNumber})
    context = {'institutionForm': institutionForm}
    return render(request, 'icparsa/secondParty/institution.html', context)


@allowed_users(allowed_roles=['admin', 'procurement'])
@login_required(login_url='log')
def updateInstitution(request, pk):
    inst = SecondParty.objects.get(id=pk)
    institutionForm = InstitutionForm(instance=inst)
    if request.method == 'POST':
        institutionForm = InstitutionForm(request.POST, instance=inst)
        if institutionForm.is_valid():
            institutionForm.save()
            return redirect('insts')
    context = {'institutionForm': institutionForm, 'inst': inst}
    return render(request, 'icparsa/secondParty/institution.html', context)


@allowed_users(allowed_roles=['admin', 'procurement'])
@login_required(login_url='log')
def deleteInstitution(request, pk):
    inst = SecondParty.objects.get(id=pk)
    if request.method == 'POST':
        inst.delete()
        return redirect('/insts')
    context = {'inst': inst}
    return render(request, 'icparsa/secondParty/delInst.html', context)


@allowed_users(allowed_roles=['admin', 'procurement'])
@login_required(login_url='log')
def searchWithCompanyName(request):
    shaka = request.GET.get('shaka', '')
    if shaka:
        institutionsList = SecondParty.objects.filter(name__icontains=shaka)
    else:
        institutionsList = SecondParty.objects.none()

    context = {'institutionsList': institutionsList, 'shaka': shaka}
    return render(request, 'icparsa/secondParty/institutions.html', context)
