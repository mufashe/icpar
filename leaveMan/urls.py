from django.urls import path

from leaveMan.views import leadDash
from leaveMan.views.leave_view import *

urlpatterns = [
    path('ld/', leadDash, name='ld'),
    path('rl/', recordLeave, name='rl'),
    path('lil/', listLeave, name='lil'),
    path('ul/<str:pk>', updateLeave, name='ul'),
    path('uls/<int:pk>/', updateLeaveStatus, name='uls'),
    path('gl/<int:pk>/', give_leave, name='gl'),
    path('ajax/loadTitle', loadTitle, name='loadTitle'),
    path('holidays/<str:country>/', holidays_view, name='holidays'),
    path('phapi/<str:country>/<int:year>/', publicHolidaysAPICaller, name='phapi'),
    path('loadleave/<int:pk>', generateLeave, name='loadleave'),

]
