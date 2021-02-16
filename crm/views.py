from django.shortcuts import render, redirect
from django.db.models import Q
from crm.forms.clientforms import (
    ClientForms,
    ContactForms,
)
from crm.forms.messageforms import (
    EmailForm,
    SmsForm,
    FilterForm
)
from .models import (
    ClientManager,
    ContactManager,
    Message,
    FilterSet
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.conf import settings
from twilio.rest import Client
from django.core.mail import send_mail, send_mass_mail

# Create your views here.


class ClientCreate(CreateView):
    '''
    this view creates clients.
    '''
    model = ClientManager
    template_name = 'taskmanager/task_create.html'
    form_class = ClientForms
    success_message = 'You have successfully created a project. Thank you'
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(ClientCreate, self).get_context_data(**kwargs)
        context['create_client'] = True
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
    success_message = 'You have successfully created a project. Thank you'
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(ContactCreate, self).get_context_data(**kwargs)
        context['create_contact'] = True
        return context

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            form.instance = self.object
            form.save()
        return super(ContactCreate, self).form_valid(form)


def communications(request):
    context = {
        'communications': True
    }
    return render(request,'crm/communications.html',context)
    	


def filter_parameter(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form=FilterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            if form.instance.search_parameter:
                q=form.instance.search_parameter
                clients=ClientManager.objects.filter(
                            Q(country__icontains=q)|
                            Q(client_location__icontains=q)|
                            Q(client_postal_address__icontains=q)| 
                            Q(client_status__icontains=q)| 
                            Q(client_name__icontains=q) | 
                            Q(client_tel_no__icontains=q)|
                            Q(client_email__icontains=q)
                )
                contacts=ContactManager.objects.filter(
                            Q(contact_name__icontains=q)|
                            Q(position__icontains=q)|
                            Q(personal_status__icontains=q)| 
                            Q(personal_tel_no__icontains=q)|
                            Q(personal_email__icontains=q) |
                            Q(service_line__icontains=q)
                )
                clients_data,contacts_data=[],[]
                for i in range(len(clients)):
                    clients_data.append(clients[i].client_name)
                for i in range(len(contacts)):
                    contacts_data.append(contacts[i].contact_name)
                form.instance.filtered_list=[clients_data,contacts_data]
            else:
                pass
                # clients=ClientManager.objects.all()
                # contacts=ContactManager.objects.all()
                # clients_data,contacts_data=[],[]
                # for i in range(len(clients)):
                #     clients_data.append(clients[i].client_name)
                # for i in range(len(contacts)):
                #     contacts_data.append(contacts[i].contact_name)
                # form.instance.filtered_list=[clients_data,contacts_data]
            
            form.save()
            return redirect('crm:communications')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FilterForm()

    return render(request, 'crm/communications.html', {'form': form,'filters':True})

def use_existing_filter(request,search_id):
    get_data=FilterSet.objects.get(id=search_id)
    get_data.pk=None
    get_data.save()
    return redirect('crm:communications')

def broadcast_sms(request):
    # if this is a POST request we need to process the form data
    client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    get_data=FilterSet.objects.last()
    get_data.user_filters=request.user
    get_data.save()
    client_data=eval(get_data.filtered_list[0])
    contact_data=eval(get_data.filtered_list[1])
    numbers_to_broadcast=[]
    get_contacts=ContactManager.objects.filter(Q(contact_name__in=contact_data))
    for contact in get_contacts:
        numbers_to_broadcast.append(contact.personal_tel_no)
    get_clients=ClientManager.objects.filter(Q(client_name__in=client_data))
    for client_ in get_clients:
        numbers_to_broadcast.append(client_.client_tel_no)
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        message_to_broadcast=request.POST.get('sms')
        # create a form instance and populate it with data from the request:
        form = SmsForm(request.POST)
        # import pdb;pdb.set_trace()
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            contact_set=form.instance.contacts
            client_set=form.instance.clients
            # ...
            contacts=contact_set.values('contact_name')
            clients=client_set.values('client_name')
            # import pdb;pdb.set_trace()
            contact_data,client_data=[],[]
            for contact_ in contacts:
                if contact_:
                    contact_data.append(contact_['contact_name'])
            for clientel in clients:
                if clientel:
                    client_data.append(clientel['client_name'])
            contacts_=ContactManager.objects.filter(contact_name__in=contact_data)
            clients_=ClientManager.objects.filter(client_name__in=client_data)

            if contact_data and not client_data:
                for con in contacts_:
                    numbers_to_broadcast.append(con.personal_tel_no)
            elif client_data and not contact_data:
                for cl in clients_:
                    numbers_to_broadcast.append(cl.client_tel_no)
            elif client_data and contact_data:
                for con in contacts_:
                    numbers_to_broadcast.append(con.personal_tel_no)
                for cl in clients_:
                    numbers_to_broadcast.append(cl.client_tel_no)
            # redirect to a new URL:
            # import pdb;pdb.set_trace()
            for recipient in numbers_to_broadcast:
                if recipient:
                    data=client.messages.create(
                        to=recipient,
                        from_=settings.TWILIO_NUMBER,
                        body=message_to_broadcast
                    )
                    db_content=Message()
                    db_content.account_sid=data.account_sid
                    db_content.api_version=data.api_version
                    db_content.sms=data.body
                    db_content.date_created=data.date_created
                    db_content.date_sent=data.date_sent
                    db_content.date_updated=data.date_updated
                    db_content.delete=data.delete
                    db_content.direction=data.direction
                    db_content.error_code=data.error_code
                    db_content.error_message=data.error_message
                    db_content.feedback=data.feedback
                    db_content.fetch=data.fetch
                    db_content.from_who=data.from_
                    db_content.media=data.media
                    db_content.messaging_service_sid=data.messaging_service_sid
                    db_content.num_media=data.num_media
                    db_content.num_segments=data.num_segments
                    db_content.price=data.price
                    db_content.price_unit=data.price_unit
                    db_content.sid=data.sid
                    db_content.status=data.status
                    db_content.subresource_uris=data.subresource_uris
                    db_content.to=data.to
                    db_content.update=data.update
                    db_content.uri=data.uri
                    db_content.save()
            return redirect('crm:communications')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SmsForm()

    return render(request, 'crm/communications.html', {'form': form ,'sms':True})


def broadcast_single_sms(request):
    # if this is a POST request we need to process the form data
    client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)

	
    if request.method == 'POST':
        message_to_broadcast=request.POST.get('sms')
        contact_id=request.POST.get('contacts')
        client_id=request.POST.get('clients')
        # import pdb;pdb.set_trace()
        if contact_id and not client_id:
            get_contact=ContactManager.objects.get(id=contact_id)
            numbers_to_broadcast=get_contact.personal_tel_no
        elif client_id and not contact_id:
            get_client=ClientManager.objects.get(id=client_id)
            numbers_to_broadcast=get_client.client_tel_no
        elif client_id and contact_id:
            get_contact=ContactManager.objects.get(id=contact_id)
            get_client=ClientManager.objects.get(id=client_id)
            numbers_to_broadcast=[get_client.client_tel_no,get_contact.personal_tel_no]
        else:
            numbers_to_broadcast='+254700701209'
        # create a form instance and populate it with data from the request:
        form = SmsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # import pdb;pdb.set_trace()
            data=client.messages.create(
                to=numbers_to_broadcast,
                from_=settings.TWILIO_NUMBER,
                body=message_to_broadcast
            )
            db_content=Message()
            db_content.account_sid=data.account_sid
            db_content.api_version=data.api_version
            db_content.sms=data.body
            db_content.date_created=data.date_created
            db_content.date_sent=data.date_sent
            db_content.date_updated=data.date_updated
            db_content.delete=data.delete
            db_content.direction=data.direction
            db_content.error_code=data.error_code
            db_content.error_message=data.error_message
            db_content.feedback=data.feedback
            db_content.fetch=data.fetch
            db_content.from_who=data.from_
            db_content.media=data.media
            db_content.messaging_service_sid=data.messaging_service_sid
            db_content.num_media=data.num_media
            db_content.num_segments=data.num_segments
            db_content.price=data.price
            db_content.price_unit=data.price_unit
            db_content.sid=data.sid
            db_content.status=data.status
            db_content.subresource_uris=data.subresource_uris
            db_content.to=data.to
            db_content.update=data.update
            db_content.uri=data.uri
            if contact_id and not client_id:
                get_contact=ContactManager.objects.get(id=contact_id)
                db_content.contacts=get_contact
            elif client_id and not contact_id:
                get_client=ClientManager.objects.get(id=client_id)
                db_content.clients=get_client
            elif client_id and contact_id:
                get_contact=ContactManager.objects.get(id=contact_id)
                get_client=ClientManager.objects.get(id=client_id)
                db_content.contacts=get_contact
                db_content.clients=get_client
            db_content.save()

            
            return redirect('crm:communications')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SmsForm()

    return render(request, 'crm/communications.html', {'form': form})

# for urls
 
def broadcast_emails(request):
    # if this is a POST request we need to process the form data
    site=request.build_absolute_uri('/crm/communications/index/')
    # create a form instance and populate it with data from the request:
    get_data=FilterSet.objects.last()
    get_data.user_filters=request.user
    get_data.save()
    # import pdb;pdb.set_trace()
    client_data=eval(get_data.filtered_list[0])
    contact_data=eval(get_data.filtered_list[1])
    emails_to_broadcast=[]
    get_contacts=ContactManager.objects.filter(Q(contact_name__in=contact_data))
    for contact in get_contacts:
        emails_to_broadcast.append(contact.personal_email)
    get_clients=ClientManager.objects.filter(Q(client_name__in=client_data))
    for client_ in get_clients:
        emails_to_broadcast.append(client_.client_email)
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        # create a form instance and populate it with data from the request:
        form = EmailForm(request.POST)
        # import pdb;pdb.set_trace()
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.instance.user_filters=request.user
            form.save()
            contact_set=form.instance.contacts
            client_set=form.instance.clients
            # ...
            contacts=contact_set.values('contact_name')
            clients=client_set.values('client_name')
            # import pdb;pdb.set_trace()
            contact_data,client_data=[],[]
            for contact_ in contacts:
                if contact_:
                    contact_data.append(contact_['contact_name'])
            for clientel in clients:
                if clientel:
                    client_data.append(clientel['client_name'])
            contacts_=ContactManager.objects.filter(contact_name__in=contact_data)
            clients_=ClientManager.objects.filter(client_name__in=client_data)
            
            if contact_data and not client_data:
                for con in contacts_:
                    emails_to_broadcast.append(con.personal_email)
            elif client_data and not contact_data:
                for cl in clients_:
                    emails_to_broadcast.append(cl.client_email)
            elif client_data and contact_data:
                for con in contacts_:
                    emails_to_broadcast.append(con.personal_email)
                for cl in clients_:
                    emails_to_broadcast.append(cl.client_email)
            # redirect to a new URL:
            # import pdb;pdb.set_trace()
            body=request.POST.get('email_body') + " go to site.. " +site
            subject=request.POST.get('email_subject')
            # message1 = (subject, body, settings.FROM_EMAIL, emails_to_broadcast)
            # message2 = (subject, body, settings.FROM_EMAIL, emails_to_broadcast)
            # import pdb;pdb.set_trace()
            # send_mass_mail((message1, message2), fail_silently=False)
            # import pdb;pdb.set_trace()

            send_mail(subject,body,settings.FROM_EMAIL,emails_to_broadcast,fail_silently=False)
            return redirect('crm:communications')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmailForm()

    return render(request, 'crm/communications.html', {'form': form,'emails':True})

def broadcast_single_email(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmailForm(request.POST)
        # check whether it's valid:
        body=request.POST.get('email_body')
        subject=request.POST.get('email_subject')
        contacts=request.POST.get('contacts')
        clients=request.POST.get('clients')
        if form.is_valid():
            send_mail(subject,body,settings.FROM_EMAIL,['tutorialcreation81@gmail.com','hesbon5600@gmail.com'],fail_silently=False)
            return redirect('crm:communications')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmailForm()

    return render(request, 'crm/communications.html', {'form': form})


