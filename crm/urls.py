from django.urls import path
from . import views

app_name='crm'

urlpatterns=[
    path('client/create/', views.ClientCreate.as_view(), name='client_create'),
    path('contact/create/', views.ContactCreate.as_view(), name='contact_create'),
	path('communications/index/',views.communications,name='communications'),
	path('communications/filters/',views.filter_parameter,name='filter_params'),
	path('communications/sms/',views.broadcast_sms,name='send_bulk_sms'),
	path('communications/sms/single/',views.broadcast_single_sms,name='send_single_sms'),
	path('communications/emails/',views.broadcast_emails,name='send_mass_email'),
	path('communications/emails/single/',views.broadcast_single_email,name='send_single_email'),
	path('communications/existing_filter/<int:search_id>/',views.use_existing_filter,name='use_existing_filter'),
]