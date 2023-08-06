from django.urls import path

from consumption.views import userChannels



urlpatterns = [
    path('channels', userChannels)
]