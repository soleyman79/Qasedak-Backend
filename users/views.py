from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout

from .forms import SignUpForm


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        validation = form.is_valid()
        if validation == 'OK':
            form.save()
            return HttpResponse('User Created Successfully')

        else:
            return HttpResponse(validation)

    else:
        return HttpResponse('only POST method allowed')

    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=f'user-{username}', password=password)
        if user:
            dj_login(request, user)
            return HttpResponse('Login Completed')
        else:
            return HttpResponse('wrong password/username')

    else:
        return HttpResponse('login with POST method')


@csrf_exempt
@login_required(login_url='loginFirst')
def logout(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('please login first')

        else:
            dj_logout(request)
            return HttpResponse('Logout Successfully')

    else:
        return HttpResponse('only POST method allowed')
    
    
def loginFirst(request):
    return HttpResponse('Login First')