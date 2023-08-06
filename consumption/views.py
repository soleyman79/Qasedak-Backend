from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from creation.models import Member, Chanel



@login_required(login_url='loginFirst')
def userChannels(request):
    if request.method == 'GET':
        user = request.user
        channelsId = Member.objects.filter(user=user).values_list('chanel', flat=True)
        channels = Chanel.objects.filter(id__in=channelsId)
        return JsonResponse({'names': list(channels.values_list('name', flat=True))})
    else:
        return HttpResponse('only GET method allowed')
