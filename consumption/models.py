from django.db import models
from django.core.validators import FileExtensionValidator



# class Content(models.Model):
#     title = models.CharField(max_length=64)
#     summary = models.CharField(max_length=64)
#     chanel = models.ForeignKey('Chanel', on_delete=models.CASCADE)
    
#     class Meta:
#         abstract = True


# class Video(Content):
#     video = models.FileField(upload_to='videos_uploaded', 
#                              null=False, 
#                              validators=[FileExtensionValidator(allowed_extensions=['avi','mp4','webm','mkv'])])


# class Photo(Content):
#     photo = models.ImageField(upload_to='photos_uploaded')
    

# class Chanel(models.Model):
#     name = models.CharField(unique=True, max_length=128)