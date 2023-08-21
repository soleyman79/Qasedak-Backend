from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from .forms import SignUpForm
from .models import Session
# from creation.models import *


@csrf_exempt
def signup(request):
    # Manager.objects.all().delete()
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        validation = form.is_valid()
        if validation == 'OK':
            form.save()
            return JsonResponse({'status': 'OK', 'message': 'User Created Successfully'})

        else:
            return JsonResponse({'status': 'ERROR', 'message': validation})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})

    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=f'user-{username}', password=password)
        if user:
            session = Session.objects.create(user=user)
            return JsonResponse({'status': 'OK', 'message': session.session})
        else:
            return JsonResponse({'status': 'ERROR', 'message': 'wrong password/username'})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        else:
            Session.objects.filter(session=session).delete()
            return JsonResponse({'status': 'OK', 'message': 'Logout Successfully'})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})