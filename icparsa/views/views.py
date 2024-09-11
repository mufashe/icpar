import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q

from icparsa.models.models import Contract, SecondParty


@login_required(login_url='log')
def home(request):
    user = request.user
    totalContracts = Contract.objects.all().count()
    canceledContracts = Contract.objects.filter(contract_status='EXPIRED').count()
    # canceledContracts = Contract.objects.filter(
    #     contractCategory__contract__expirationDate__lte=datetime.datetime.now()).count()
    signedContracts = Contract.objects.filter(contract_status='SIGNED').count()
    # signedContracts = Contract.objects.filter(
    #     contractCategory__contract__expirationDate__gt=datetime.datetime.now()).count()

    listInstitutions = SecondParty.objects.all()
    listContracts = Contract.objects.all()
    admin = Q(groups__name='admin')
    end_user = Q(groups__name='end_user')
    procurement = Q(groups__name='procurement')
    leave = Q(groups__name='leaveManager')
    correspond = Q(groups__name='correspondence')

    admins = User.objects.filter(admin)
    end_users = User.objects.filter(end_user)
    leaveManager = User.objects.filter(leave)
    correspondenceManager = User.objects.filter(correspond)
    procurementManager = User.objects.filter(procurement)

    is_correspondenceManager = request.user.groups.filter(name='correspondence').exists()
    is_leaveManager = request.user.groups.filter(name__iexact='leaveManager').exists()
    is_admin = request.user.groups.filter(name__iexact='admin').exists()

    contracts = Contract.objects.all()
    contractReport = {}
    for c in contracts:
        contractReport[c.contract_status] = contractReport.get(c.contract_status, 0) + 1

    context = {'totalContracts': totalContracts, 'canceledContracts': canceledContracts,
               'signedContracts': signedContracts, 'listInstitutions': listInstitutions, 'listContracts': listContracts,
               'end_users': end_users, 'admins': admins, 'contracts': contracts, 'contractReport': contractReport,
               'is_leaveManager': is_leaveManager, 'is_correspondenceManager': is_correspondenceManager,
               'procurementManager': procurementManager, 'is_admin': is_admin, 'leaveManager': leaveManager,
               'correspondenceManager': correspondenceManager}
    return render(request, 'icparsa/template/dashboard.html', context)


# @login_required(login_url='log')
# def nav_setting(request):
#     logged_in_user = request.user
#     admin = Q(groups__name='admin')
#     end_user = Q(groups__name='end_user')
#     procurement = Q(groups__name='procurement')
#     correspondences = Q(groups__name='correspondence')
#     leaveMan = Q(groups__name='leaveManager')
#
#     AllowedToContract = User.objects.filter(admin | procurement)
#     contractViewOnly = User.objects.filter(end_user)
#     leaveViewOnly = User.objects.filter(end_user)
#     correspondenceManagers = User.objects.filter(correspondences | admin)
#
#     is_correspondenceManager = request.user.groups.filter(name='correspondence').exists()
#     is_leaveManager = request.user.groups.filter(name__iexact='leaveManager').exists()
#
#     correspondenceViewOnly = User.objects.filter(end_user)
#     leaveManagers = User.objects.filter(leaveMan | admin)
#
#     user_groups = request.user.groups.values_list('name', flat=True)
#
#     admins = User.objects.filter(admin)
#     end_users = User.objects.filter(end_user)
#     procurements = User.objects.filter(procurement)
#     print('****************', is_leaveManager, '*******************************')
#
#     context = {'logged_in_user': logged_in_user, 'admins': admins, 'end_users': end_users,
#                'AllowedToContract': AllowedToContract, 'procurements': procurements, 'leaveManagers': leaveManagers,
#                'contractViewOnly': contractViewOnly, 'leaveViewOnly': leaveViewOnly,
#                'correspondenceViewOnly': correspondenceViewOnly, 'correspondenceManagers': correspondenceManagers,
#                'is_correspondenceManager': is_correspondenceManager, 'user_groups': user_groups,
#                'is_leaveManager': is_leaveManager}
#     return render(request, 'icparsa/template/main.html', context)


@login_required(login_url='log')
def listCustomers(request):
    institutionsList = SecondParty.objects.all()
    context = {'institutionsList': institutionsList}
    return render(request, 'icparsa/secondParty/institutions.html', context)
