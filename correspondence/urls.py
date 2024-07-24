from django.urls import path

from correspondence.views.corrrespondenceView import recordCorrespondence, listCorrespondence, deleteCorrespondence, \
    updateCorrespondence, loadDepartmentUnit

urlpatterns = [

    path('cor/', recordCorrespondence, name='cor'),
    path('lic/', listCorrespondence, name='lic'),
    path('upco/<str:pk>', updateCorrespondence, name='upco'),
    path('dec/<str:pk>', deleteCorrespondence, name='dec'),
    path('ajax/load_unit', loadDepartmentUnit, name='loadDepartmentUnit'),
]
