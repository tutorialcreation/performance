from django.contrib import admin
from .models import ClientManager,ContactManager

# Register your models here.
admin.site.register(ClientManager)
admin.site.register(ContactManager)
