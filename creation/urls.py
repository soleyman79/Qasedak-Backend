from django.urls import path
from .views import *


urlpatterns = [
    path('chanel', createChanel),
    path('content', createContent),
]