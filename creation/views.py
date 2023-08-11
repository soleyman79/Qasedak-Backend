from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from users.models import Session

from .models import Chanel, Member, Owner
from consumption.models import Text



@csrf_exempt
def createChanel(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        name = request.POST['name']
        description = request.POST['description']
        user = Session.objects.get(session=session).user
        try:
            chanel = Chanel.objects.create(name=name, description=description)
            owner = Owner.objects.create(chanel=chanel)
            Member.objects.create(user=user, chanel=chanel, producer=owner)
            return JsonResponse({'status': 'OK', 'message': 'Chanel Created'})
        except:
            return JsonResponse({'status': 'ERROR', 'message': 'Duplicate Chanel Name'})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})
    

@csrf_exempt
def createContent(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        chanelName = request.POST['chanel']
        title = request.POST['title']
        summary = request.POST['summary']
        text = request.POST['text']
        
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel does not exist'})
        
        chanel = Chanel.objects.get(name=chanelName)
        if not Member.objects.filter(Q(user=user) & Q(chanel=chanel)):
            return JsonResponse({'status': 'ERROR', 'message': 'You are not a Member'})
        
        member = Member.objects.get(Q(user=user) & Q(chanel=chanel))
        if member.producer is None:
            return JsonResponse({'status': 'ERROR', 'message': 'You are not a Producer'})
        else:
            Text.objects.create(title=title, summary=summary, chanel=chanel, text=text)
            return JsonResponse({'status': 'OK', 'message': 'Content Added'})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})