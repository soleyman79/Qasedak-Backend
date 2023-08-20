from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F

from users.models import Session

from .models import *
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
        pro = request.POST['pro']
        
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel does not exist'})
        
        chanel = Chanel.objects.get(name=chanelName)
        if not Member.objects.filter(Q(user=user) & Q(chanel=chanel)):
            return JsonResponse({'status': 'ERROR', 'message': 'You are not a Member'})
        
        member = Member.objects.get(Q(user=user) & Q(chanel=chanel))
        if member.producer is None:
            return JsonResponse({'status': 'ERROR', 'message': 'You are not a Producer'})
        else:
            Text.objects.create(title=title, summary=summary, chanel=chanel, text=text, pro=pro)
            return JsonResponse({'status': 'OK', 'message': 'Content Added'})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})

    
@csrf_exempt
def getMembers(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        chanelName = request.POST['chanel_name']
        
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel does not exist'})
        
        chanel = Chanel.objects.get(name=chanelName)
        if not Member.objects.filter(Q(user=user) & Q(chanel=chanel) & Q(producer__chanel=chanel)).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'You do not have permission'})
        
        return JsonResponse({'status': 'OK',
                             'members': list(Member.objects.filter(chanel=chanel).values_list('user__username', flat=True))})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})
    
@csrf_exempt
def getManagers(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        chanelName = request.POST['chanel_name']
        
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel does not exist'})
        
        chanel = Chanel.objects.get(name=chanelName)
        if not Member.objects.filter(Q(user=user) & Q(chanel=chanel) & Q(producer__chanel=chanel)).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'You do not have permission'})
        
        managers = Manager.objects.filter(chanel=chanel)
        
        return JsonResponse({'status': 'OK',
                             'managers': list(managers.values_list('member', flat=True)),
                             'profits': list(managers.values_list('profit', flat=True))})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})
    
    
@csrf_exempt
def updateChanel(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        chanelName = request.POST['chanel_name']
        
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel does not exist'})
        
        chanel = Chanel.objects.get(name=chanelName)
        if not Member.objects.filter(Q(user=user) & Q(chanel=chanel) & Q(producer__chanel=chanel)).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'You do not have permission'})
        
        chanel.subscriptionPrice1 = request.POST['1']
        chanel.subscriptionPrice2 = request.POST['3']
        chanel.subscriptionPrice3 = request.POST['6']
        chanel.subscriptionPrice4 = request.POST['12']
        chanel.save()
        
        return JsonResponse({'status': 'OK',
                             'message': 'Chanel Info Updated'})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})
    
    
@csrf_exempt
def addManager(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        chanelName = request.POST['chanel_name']
        
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel does not exist'})
        chanel = Chanel.objects.get(name=chanelName)

        username = request.POST['username']
        if not User.objects.filter(username=username):
            return JsonResponse({'status': 'ERROR', 'message': 'User does not exist'})
        
        if not Member.objects.filter(Q(user__username=username) & Q(chanel=chanel)).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'This user is not a Member'})
        
        if user.username == username:
            return JsonResponse({'status': 'ERROR', 'message': 'Owner can not be a Manager'})
        
        profit = request.POST['profit']
        if Member.objects.filter(Q(user=user) & Q(chanel=chanel) & Q(producer__chanel=chanel)).exists():
            boss = Member.objects.get(Q(user=user) & Q(chanel=chanel) & Q(producer__chanel=chanel))
            if boss.getProducer() == 'Manager':
                return JsonResponse({'status': 'ERROR', 'message': 'You do not have permission'})
            else:
                manager = Manager.objects.create(chanel=chanel, profit=profit)
                member = Member.objects.get(user__username=username)
                member.producer = manager
                member.save()
                return JsonResponse({'status': 'OK', 'message': 'Manager Added'})
        

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})