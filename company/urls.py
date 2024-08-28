from django.urls import path

from company.views.companyEmployeeView import saveEmployee, listEmployee, updateEmployee, recordSystemUserAsEmployee, \
    loadTitle
from company.views.companyView import createCompany, listCompany, updateCompany, deleteCompany
from company.views.departmentView import createDepartment, listDepartment, updateDepartment, deleteDepartment
from company.views.titleView import createCompanyTitle, listTitle, updateTitle, deleteTitle, load_unit, loadDepartment
from company.views.unitView import createUnit, listUnit, updateUnit, deleteUnit, loadUnit
from company.views.userAsEmployeeView import createSignature, displayEmployeeSignature

urlpatterns = [
    path('tit', createCompanyTitle, name='tit'),
    path('lt', listTitle, name='lt'),
    path('upti<str:pk>', updateTitle, name='upti'),
    path('delt<str:pk>', deleteTitle, name='delt'),

    path('dep', createDepartment, name='dep'),
    path('ld', listDepartment, name='ld'),
    path('upde<str:pk>/', updateDepartment, name='upde'),
    path('deld<str:pk>/', deleteDepartment, name='deld'),

    path('cop', createCompany, name='cop'),
    path('lc/', listCompany, name='lc'),
    path('upco/<str:pk>', updateCompany, name='upco'),
    path('delc/<str:pk>', deleteCompany, name='delc'),

    path('cem/', saveEmployee, name='cem'),
    path('lem/', listEmployee, name='lem'),
    path('upem/<str:pk>', updateEmployee, name='upem'),
    path('syem/<int:pk>', recordSystemUserAsEmployee, name='syem'),

    path('cun/', createUnit, name='cun'),
    path('lun/', listUnit, name='lun'),
    path('upun/<str:pk>', updateUnit, name='upun'),
    path('delun/<str:pk>', deleteUnit, name='delun'),
    path('cresig/', createSignature, name='cresig'),
    path('li_em_si/<str:pk>/signature/', displayEmployeeSignature, name='li_em_si'),

    path('ajax/loadUnitDropdown', load_unit, name='loadUnit'),
    path('ajax/loadDepartmentDropdown', loadDepartment, name='load_department'),
    path('ajax/loadTitleDropdown', loadTitle, name='loadTitle')

]
