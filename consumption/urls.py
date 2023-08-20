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
]