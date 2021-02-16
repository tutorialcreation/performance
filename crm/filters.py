from django.contrib.auth.models import User
from .models import ClientManager,ContactManager
import django_filters

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model=ClientManager
        fields=[
            'client_name',
            'country',
            'client_tel_no',
            'client_email',
            'client_location',
            'client_status',
            'nature_of_assignment',
            'contract_period',
        ]


class ContactFilter(django_filters.FilterSet):
    class Meta:
        model=ContactManager
        fields=[
            'contact_name',
            'position',
            'personal_tel_no',
            'personal_email',
            'personal_status',
            'client',
            'service_line',
        ]
        