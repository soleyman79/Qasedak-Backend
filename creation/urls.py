from django.urls import path
from .views import createChanel, createContent


urlpatterns = [
    path('chanel', createChanel),
    path('content', createContent),
]