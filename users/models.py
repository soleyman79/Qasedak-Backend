from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(primary_key=True, max_length=128, unique=True)
    
    email = models.EmailField(_('Email Address'), 
                              null=True, 
                              blank=True)
    
    phone = models.CharField(_('Phone Number'), 
                             validators=[RegexValidator('^09\d{9}$', message='Invalid Phone Number')],
                             max_length=16, 
                             null=True, 
                             blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generateUsername(self.email, self.phone)
        super().save(*args, **kwargs)

        
def generateUsername(email, phone):
    if phone is None:
        return f'user-{email}'
    else:
        return f'user-{phone}'
    