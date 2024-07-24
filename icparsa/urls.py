from django.urls import include, path

from . import views
from .views import contractView, institutionView, loginView, spTypeView, departmentView, departmentMemberView, \
    notificationView, contractSettingView
from .views.notificationView import sendEmailNotification

urlpatterns = [

    path('', views.home, name='home'),
    path('icparsa/', include("django.contrib.auth.urls")),

    path('con/', contractView.recordContract, name="cont"),
    path('upcon/<str:pk>', contractView.updateContract, name="upcon"),
    path('delCo/<int:pk>', contractView.deleteContract, name="delCo"),
    path('conts/', contractView.listContracts, name="conts"),
    path('srch/', contractView.searchWithDates, name='srch'),
    path('sic/', contractView.searchCompanyName, name='sic'),
    path('upStat/<str:pk>', contractView.updateContractStatus, name='upStat'),
    path('excon/', contractView.exportContractExport, name='excon'),
    path('renewCon/<int:pk>', contractView.contractRenew, name='renewCon'),

    path('inst/', institutionView.recordInstitute, name="inst"),
    path('upins/<int:pk>', institutionView.updateInstitution, name="upins"),
    path('insts/', views.listCustomers, name="insts"),
    path('delinst/<int:pk>', institutionView.deleteInstitution, name="delinst"),
    path('schin/', institutionView.searchWithCompanyName, name="schin"),
    path('spt/', spTypeView.createNewType, name='spt'),

    path('dep/', departmentView.createDepartment, name='dep'),
    path('ldep/', departmentView.listDepartment, name='ldep'),
    path('dem/', departmentMemberView.createDepartmentMember, name='dem'),
    path('ldem/', departmentMemberView.listDepartmentMember, name='ldem'),
    path('ajax/load_department_members', departmentMemberView.load_department_members,
         name='load_department_members_url'),
    path('updem/<str:pk>', departmentMemberView.updateDepartmentMember, name='updem'),
    path('updep/<str:pk>', departmentView.updateDepartment, name='updep'),

    path('log/', loginView.loger, name='log'),
    path('lout/', loginView.signe_out, name='lout'),
    path('reg/', loginView.registerPage, name='reg'),
    path('lsu/', loginView.listSystemUsers, name='lsu'),

    path('note/', notificationView.sendEmail, name='note'),
    path('conset/', contractSettingView.setupContract, name='conset'),
    path('liconset/', contractSettingView.listContractSetup, name='liconset'),
    path('upConSet/<str:pk>', contractSettingView.updateContractSetup, name='upConSet'),
    path('delConSet/<str:pk>', contractSettingView.deleteContractSetup, name='delConSet'),
    path('consetName/', contractSettingView.createContractSettingName, name='consetName'),
    path('LiCoSeNa/', contractSettingView.listContractSettingName, name='LiCoSeNa'),
    path('upLiCoSeNa/<str:pk>/', contractSettingView.updateContractSettingName, name='upLiCoSeNa'),
    path('ajax/load_contract_type', contractSettingView.loadContractSettingType,
         name='load_contract_type_url'),
]
