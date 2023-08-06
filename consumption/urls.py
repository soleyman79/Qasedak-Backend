from django.urls import path

from consumption.views import userChannels, searchChanel



urlpatterns = [
    path('channels', userChannels),
    path('search_chanel', searchChanel)
]