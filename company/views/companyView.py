from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from company.forms.companyForm import CompanyForm
from company.models import Company
from icparsa.decorators import allowed_users


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def createCompany(request):
    next_number = Company.objects.all().count() + 1
    companyForm = CompanyForm(initial={'number': next_number})
    if request.method == 'POST':
        companyForm = CompanyForm(request.POST)
        companyForm.save()
        return redirect('lc')
    context = {'companyForm': companyForm}
    return render(request, 'company/company.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def listCompany(request):
    companyList = Company.objects.all()
    context = {'companyList': companyList}
    return render(request, 'company/listCompany.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def updateCompany(request, pk):
    company = Company.objects.get(id=pk)
    companyForm = CompanyForm(instance=company)
    if request.method == 'POST':
        companyForm = CompanyForm(request.POST, instance=company)
        if companyForm.is_valid():
            companyForm.save()
            return redirect('lc')

    context = {'companyForm': companyForm, 'company': company}
    return render(request, 'company/company.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin'])
def deleteCompany(request, pk):
    company = Company.objects.get(id=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('lt')
    context = {'company': company}
    return render(request, 'company/deleteCompany.html', context)
