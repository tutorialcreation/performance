from django.shortcuts import render
from crm.forms.clientforms import (
    ClientForms,
    ContactForms
)
from .models import (
    ClientManager,
    ContactManager
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from twilio.rest import Client
from django.core.mail import send_mail,send_mass_mail

# Create your views here.
class ClientCreate(CreateView):
    '''
    this view creates clients.
    '''
    model = ClientManager
    template_name = 'taskmanager/task_create.html'
    form_class = ClientForms
    success_message='You have successfully created a project. Thank you'
    success_url = '.'


    def get_context_data(self, **kwargs):
        context = super(ClientCreate, self).get_context_data(**kwargs)
        context['create_client']=True
        return context

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            form.instance = self.object
            form.save()
        return super(ClientCreate, self).form_valid(form)

class ContactCreate(CreateView):
    '''
    this view creates contact persons
    '''
    model = ContactManager
    template_name = 'taskmanager/task_create.html'
    form_class = ContactForms
    success_message='You have successfully created a project. Thank you'
    success_url = '.'


    def get_context_data(self, **kwargs):
        context = super(ContactCreate, self).get_context_data(**kwargs)
        context['create_contact']=True
        return context

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            form.instance = self.object
            form.save()
        return super(ContactCreate, self).form_valid(form)
		
		
def communications(request):
	context={}
	return render(request,'crm/communications.html',context)
		
def broadcast_sms(request):
	context={}
	message_to_broadcast=(
		"Hey Hezzy weren't we to have a sync today???...."
	)
	client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
	numbers_to_broadcast=['+254700701209','+254727737299']
	for recipient in numbers_to_broadcast:
		if recipient:
			client.messages.create(
				to=recipient,
				from_=settings.TWILIO_NUMBER,
				body=message_to_broadcast
			)
	return render(request,'crm/communications.html',context)


def broadcast_emails(request):
	context={}
	message1 = ('Subject here', 'Here is the message', settings.FROM_EMAIL, ['tutorialcreation81@gmail.com', 'hesbon5600@gmail.com'])
	message2 = ('Another Subject', 'Here is another message', settings.FROM_EMAIL, ['hesbon5600@gmail.com'])
	send_mass_mail((message1, message2), fail_silently=False)
	return render(request,'crm/communications.html',context)