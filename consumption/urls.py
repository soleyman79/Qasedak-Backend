from django.urls import path

from consumption.views import *



urlpatterns = [
    path('channels', userChannels),
    path('search_chanel', searchChanel),
    path('messages', chanelMessages),
    path('message', showMessage),
    path('join', joinChanel),
    path('chanel_info', chanelInfo),
    path('my_subs', mySubscriptions),
    path('credit', credit),
    path('leave', leaveChanel),
    path('buy_sub', buySubscription)
]