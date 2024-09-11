from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from icparsa.decorators import allowed_users
from icparsa.forms.SPTypeForm import SecondPartyForm
from icparsa.models.secondPartyType import SecondPartyType


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def createNewType(request):
    nextNumber = SecondPartyType.objects.all().count() + 1
    secondPartyForm = SecondPartyForm(initial={'number': nextNumber})
    if request.method == 'POST':
        secondPartyForm = SecondPartyForm(request.POST)
        secondPartyForm.save()
        return redirect('spt')
    context = {'secondPartyForm': secondPartyForm}
    return render(request, 'icparsa/secondParty/type/sctype.html', context)


def listSecondPartyType(request):
    secondPartyTypes = SecondPartyType.objects.all()
    context = {'secondPartyTypes': secondPartyTypes}
    return render(request, 'icparsa/secondParty/type/listsecondPartyType.html', context)
