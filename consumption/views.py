from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from creation.models import Member, Chanel
from users.models import Session



def userChannels(request):
    if request.method == 'POST':
        session = request.POST['session']
        if not Session.objects.filter(session=session).exists():
            return HttpResponse('Login First')
        
        user = Session.objects.get(session=session)
        channelsId = Member.objects.filter(user=user).values_list('chanel', flat=True)
        channels = Chanel.objects.filter(id__in=channelsId)
        return JsonResponse({'names': list(channels.values_list('name', flat=True))})
    else:
        return HttpResponse('only POST method allowed')
