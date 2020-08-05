from django.urls import path
from . import views

app_name='crm'

urlpatterns=[
    path('client/create/', views.ClientCreate.as_view(), name='client_create'),
    path('contact/create/', views.ContactCreate.as_view(), name='contact_create'),
	path('communications/index/',views.communications,name='communications'),
	path('communications/sms/',views.broadcast_sms,name='send_bulk_sms'),
	path('communications/emails/',views.broadcast_emails,name='send_mass_email'),
]