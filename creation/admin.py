from django.contrib import admin
from .models import Manager


class ManagerAdmin(admin.ModelAdmin):
    list_display = ['profit', 'chanel']

admin.site.register(Manager, ManagerAdmin)

