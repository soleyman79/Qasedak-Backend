from django.urls import path
from .views import *


urlpatterns = [
    path('chanel', createChanel),
    path('content', createContent),
    path('get_members', getMembers),
    path('get_managers', getManagers),
    path('update_chanel', updateChanel),
    path('add_manager', addManager),
    path('set_profit', setProfit),
    path('add_credit', addCredit),
]