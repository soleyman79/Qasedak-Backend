from django.db import models
from users.models import User
from consumption.models import Chanel

    
    
class Producer(models.Model):
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE)
    

class Owner(Producer):
    profit = models.SmallIntegerField(null=True)


class Manager(Producer):
    profit = models.SmallIntegerField(null=False)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True)
    
    def getProducer(self):
        return self.producer.__class__.__subclasses__()[0].__name__


class Subscription(models.Model):
    subType = models.CharField(max_length=1, default="1")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    remaining = models.SmallIntegerField()
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE)