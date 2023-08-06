from django.contrib import admin
from .models import Chanel



class ChanelAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Chanel, ChanelAdmin)
