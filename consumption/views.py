from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from creation.models import Member, Chanel
from users.models import Session



@csrf_exempt
def userChannels(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return HttpResponse('Login First')
        
        user = Session.objects.get(session=session).user
        channelsId = Member.objects.filter(user=user).values_list('chanel', flat=True)
        channels = Chanel.objects.filter(id__in=channelsId)
        return JsonResponse({'names': list(channels.values_list('name', flat=True)),
                             'description': list(channels.values_list('description', flat=True))})
    else:
        return HttpResponse('only POST method allowed')
    

@csrf_exempt
def searchChanel(request):
    if request.method == 'POST':
        session = request.POST['session']
        search = request.POST['search']
        if not Session.objects.filter(session=session).exists():
            return HttpResponse('Login First')
        
        user = Session.objects.get(session=session).user
        channels = Chanel.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return JsonResponse({'names': list(channels.values_list('name', flat=True)),
                             'description': list(channels.values_list('description', flat=True))})
    else:
        return HttpResponse('only POST method allowed')
    
    
@csrf_exempt
def joinChanel(request):
    if request.method == 'POST':
        session = request.POST['session']
        chanelName = request.POST['chanel_name']
        if not Session.objects.filter(session=session).exists():
            return HttpResponse('Login First')
        
        user = Session.objects.get(session=session).user
        if not Chanel.objects.filter(name=chanelName).exists():
            return JsonResponse({'status': 'ERROR', 'message': 'Chanel not Exists'})
        
        chanel = Chanel.objects.get(name=chanelName)
        if Member.objects.filter(Q(chanel=chanel) & Q(user=user)):
            return JsonResponse({'status': 'ERROR', 'message': 'You are already a Member'})
        else:
            Member.objects.create(user=user, chanel=chanel)
            return JsonResponse({'status': 'OK', 'message': 'You Joined'})
    else:
        return HttpResponse('only POST method allowed')
    
    

