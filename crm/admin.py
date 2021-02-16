from django.contrib import admin
from .models import (
    ClientManager,ContactManager,
    Message,FilterSet
)

# Register your models here.
admin.site.register(ClientManager)
admin.site.register(ContactManager)
admin.site.register(Message)
admin.site.register(FilterSet)


