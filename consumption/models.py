from django.db import models
from django.core.validators import FileExtensionValidator



class Content(models.Model):
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=64)
    chanel = models.ForeignKey('Chanel', on_delete=models.CASCADE)
    
    class Meta:
        abstract = True


class Text(Content):
    text = models.TextField(max_length=512)


class Video(Content):
    video = models.FileField(upload_to='videos_uploaded', 
                             null=False, 
                             validators=[FileExtensionValidator(allowed_extensions=['avi','mp4','webm','mkv'])])


class Photo(Content):
    photo = models.ImageField(upload_to='photos_uploaded')
    

class Chanel(models.Model):
    name = models.CharField(unique=True, max_length=128)
    description = models.CharField(max_length=512)
    subscriptionPrice1 = models.SmallIntegerField(null=True, blank=True)
    subscriptionPrice2 = models.SmallIntegerField(null=True, blank=True)
    subscriptionPrice3 = models.SmallIntegerField(null=True, blank=True)
    subscriptionPrice4 = models.SmallIntegerField(null=True, blank=True)

  
    
class Subscription(models.Model):
    remaining = models.SmallIntegerField()
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE)