from django.urls import path
from .views import signup, login, logout, loginFirst


urlpatterns = [
    path('signup', signup),
    path('login', login),
    path('logout', logout),
    path('loginFirst', loginFirst, name='loginFirst')
]
