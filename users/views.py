from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from .forms import SignUpForm
from .models import Session


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
            session = Session.objects.create(user=user)
            return JsonResponse({'status': 'OK', 'message': session.session})
        else:
            return HttpResponse('wrong password/username')

    else:
        return HttpResponse('login with POST method')


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return HttpResponse('Login First')
        
        else:
            Session.objects.filter(session=session).delete()
            return HttpResponse('Logout Successfully')

    else:
        return HttpResponse('only POST method allowed')