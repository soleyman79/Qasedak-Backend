from django.urls import path
from .views import createChanel


urlpatterns = [
    path('chanel', createChanel)
]