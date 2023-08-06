from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Chanel



@csrf_exempt
@login_required(login_url='loginFirst')
def createChanel(request):
    if request.method == 'POST':
        name = request.POST['name']
        try:
            Chanel.objects.create(name=name)
            return HttpResponse('Chanel Created')
        except:
            return HttpResponse('Duplicate Chanel Name')

    else:
        return HttpResponse('only POST method allowed')
