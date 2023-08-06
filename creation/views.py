from django.http import HttpResponse
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
            return HttpResponse('Login First')
        
        name = request.POST['name']
        user = Session.objects.get(session=session).user
        try:
            chanel = Chanel.objects.create(name=name)
            owner = Owner.objects.create(chanel=chanel)
            Member.objects.create(user=user, chanel=chanel, producer=owner)
            return HttpResponse('Chanel Created')
        except:
            return HttpResponse('Duplicate Chanel Name')

    else:
        return HttpResponse('only POST method allowed')
    

@csrf_exempt
def createContent(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return HttpResponse('Login First')
        
        user = Session.objects.get(session=session).user
        chanelName = request.POST['chanel']
        title = request.POST['title']
        summary = request.POST['summary']
        text = request.POST['text']
        
        if not Chanel.objects.filter(name=chanelName).exists():
            return HttpResponse('Chanel does not exist')
        
        chanel = Chanel.objects.get(name=chanelName)
        if not Member.objects.filter(Q(user=user) & Q(chanel=chanel)):
            return HttpResponse('You are not a Member')
        
        member = Member.objects.get(Q(user=user) & Q(chanel=chanel))
        if member.producer is None:
            return HttpResponse('You are not a Producer')
        else:
            Text.objects.create(title=title, summary=summary, chanel=chanel, text=text)
            return HttpResponse('Content Added')

    else:
        return HttpResponse('only POST method allowed')