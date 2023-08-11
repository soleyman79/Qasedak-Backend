from django.urls import path

from consumption.views import userChannels, searchChanel, chanelMessages, showMessage



urlpatterns = [
    path('channels', userChannels),
    path('search_chanel', searchChanel),
    path('messages', chanelMessages),
    path('message', showMessage)
]