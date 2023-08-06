from django.db import models
from django.db import models
from users.models import User
from consumption.models import Chanel

    
    
class Producer(models.Model):
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE)
    

class Owner(Producer):
    pass


class Manager(Producer):
    profit = models.SmallIntegerField(null=False, blank=False)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True)