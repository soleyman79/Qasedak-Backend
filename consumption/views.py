from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from creation.models import *
from users.models import Session
from .models import Text



@csrf_exempt
def userChannels(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        channelsId = Member.objects.filter(user=user).values_list('chanel', flat=True)
        channels = Chanel.objects.filter(id__in=channelsId)
        return JsonResponse({'status': 'OK',
                             'names': list(channels.values_list('name', flat=True)),
                             'descriptions': list(channels.values_list('description', flat=True))})
    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})
    

@csrf_exempt
def searchChanel(request):
    if request.method == 'POST':
        session = request.POST['session']
        search = request.POST['search']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        channels = Chanel.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return JsonResponse({'status': 'OK',
                             'names': list(channels.values_list('name', flat=True)),
                             'descriptions': list(channels.values_list('description', flat=True))})
    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})
    
  
@csrf_exempt
def joinChanel(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        chanelName = request.POST['chanel_name']
        
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel does not exist'})
        
        chanel = Chanel.objects.get(name=chanelName)
        if Member.objects.filter(Q(user=user) & Q(chanel=chanel)):
            return JsonResponse({'status': 'ERROR', 'message': 'You are already a Member'})
        
        Member.objects.create(user=user, chanel=chanel)
        return JsonResponse({'status': 'OK', 'message': 'Joined Successfully'})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})

    
@csrf_exempt
def chanelMessages(request):
    if request.method == 'POST':
        session = request.POST['session']
        chanelName = request.POST['chanel_name']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel not Exists'})
        
        chanel = Chanel.objects.get(name=chanelName)
        if not Member.objects.filter(Q(chanel=chanel) & Q(user=user)).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'You are not a Member'})
        else:
            contetns = Text.objects.filter(chanel=chanel) # TODO role: 'owner', 'manager', 'member'
            role = 'member'
            owner = Owner.objects.get(chanel=chanel)
            managers = Manager.objects.filter(chanel=chanel)
            
            if Member.objects.get(chanel=chanel, producer=owner).user == user:
                role = 'owner'
            elif Member.objects.filter(Q(user=user) & Q(producer__in=managers)).exists():
                role = 'manager'

            return JsonResponse({'status': 'OK',
                                 'role': role,
                                 'ids': list(contetns.values_list('id', flat=True)), 
                                 'titles': list(contetns.values_list('title', flat=True)), 
                                 'summaries': list(contetns.values_list('summary', flat=True)), 
                                 'pros': list(contetns.values_list('pro', flat=True))})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})


@csrf_exempt
def showMessage(request):
    if request.method == 'POST':
        session = request.POST['session']
        messageId = request.POST['id']
        if not Session.objects.filter(session=session).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Login First'})
        
        user = Session.objects.get(session=session).user
        if not Text.objects.filter(id=messageId).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Message not Exist'})
        
        content = Text.objects.get(id=messageId)
        chanel = content.chanel
        if not Member.objects.filter(Q(user=user) & Q(chanel=chanel)).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'You are not a Member'})
        
        if content.pro and not (Subscription.objects.filter(Q(member__user=user) & Q(chanel=chanel)).exists() or 
                                Member.objects.filter(Q(chanel=chanel) & Q(producer__isnull=False)).exists()):
            return JsonResponse({'status': 'ERROR', 'message': 'This Content is PRO'})

        return JsonResponse({'status': 'OK', 
                             'title': content.title,
                             'text': content.text})

    else:
        return JsonResponse({'status': 'ERROR', 'message': 'only POST method allowed'})