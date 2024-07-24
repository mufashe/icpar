from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from icparsa.decorators import allowed_users
from icparsa.forms.contractSettingForm import ContractSettingForm, ContractSettingNameForm
from icparsa.models.contractSetting import ContractSetting, ContractSettingName


def calculateRemindingTime(expiration_days):
    if expiration_days < 5:
        return 1
    elif 5 <= expiration_days < 15:
        return 3
    else:
        return 5


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def setupContract(request):
    contractSettingForm = ContractSettingForm()
    if request.method == 'POST':
        contractSettingForm = ContractSettingForm(request.POST)
        if contractSettingForm.is_valid():
            contractSetting = contractSettingForm.save(commit=False)
            expirationDays = contractSetting.expirationDays
            contractSetting.remindingTimes = calculateRemindingTime(expirationDays)
            # contractSettingForm.save()
            contractSetting.save()
        return redirect('liconset')
    context = {'contractSettingForm': contractSettingForm}
    return render(request, 'icparsa/settings/system/contractSetting.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['procurement', 'admin'])
def createContractSettingName(request):
    next_number = ContractSettingName.objects.all().count() + 1
    contractSettingNameForm = ContractSettingNameForm(initial={'number': next_number})
    if request.method == 'POST':
        contractSettingNameForm = ContractSettingNameForm(request.POST)
        if contractSettingNameForm.is_valid():
            contractSettingNameForm.save()
        return redirect('conset')
    context = {'contractSettingNameForm': contractSettingNameForm}
    return render(request, 'icparsa/settings/system/contractSettingName.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def listContractSetup(request):
    contractSetups = ContractSetting.objects.all()
    context = {'contractSetups': contractSetups}
    return render(request, 'icparsa/settings/system/listContractSetting.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def listContractSettingName(request):
    contractSettingName = ContractSettingName.objects.all()
    context = {'contractSettingName': contractSettingName}
    return render(request, 'icparsa/settings/system/listContractSettingName.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def updateContractSetup(request, pk):
    conSet = ContractSetting.objects.get(id=pk)
    conSetForm = ContractSettingForm(instance=conSet)
    if request.method == 'POST':
        conSetForm = ContractSettingForm(request.POST, instance=conSet)
        if conSetForm.is_valid():
            conSetForm.save()
            return redirect('liconset')

    context = {'contractSettingForm': conSetForm, 'conSet': conSet}
    return render(request, 'icparsa/settings/system/contractSetting.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def updateContractSettingName(request, pk):
    conSet = ContractSettingName.objects.get(id=pk)
    conSetForm = ContractSettingNameForm(instance=conSet)
    if request.method == 'POST':
        conSetForm = ContractSettingNameForm(request.POST, instance=conSet)
        if conSetForm.is_valid():
            conSetForm.save()
            return redirect('LiCoSeNa')

    context = {'contractSettingNameForm': conSetForm, 'conSet': conSet}
    return render(request, 'icparsa/settings/system/contractSettingName.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def deleteContractSetup(request, pk):
    conSetToDel = ContractSetting.objects.get(id=pk)
    if request.method == 'POST':
        conSetToDel.delete()
        return redirect('liconset')
    context = {'conSetToDel': conSetToDel}
    return render(request, 'icparsa/settings/system/delConSettings.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['procurement', 'admin'])
def loadContractSettingType(request):
    contractName_id = request.GET.get('contractName_id')
    contractType = ContractSetting.objects.filter(contractName_id=contractName_id)
    context = {'contractType': contractType}
    return render(request, 'icparsa/settings/system/contractTypeDropDown.html', context)
