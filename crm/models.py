from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.


class ClientManager(models.Model):
    STATUS_CHOICES=(
        ('E','Existing'),
        ('P','Potential'),
        ('F','Former'),
    )
    client_name=models.CharField(max_length=1028)
    country=models.CharField(max_length=1028)
    client_tel_no=models.CharField(max_length=60)
    client_email=models.EmailField()
    client_location=models.CharField(max_length=200)
    client_postal_address=models.CharField(max_length=350)
    client_status=models.CharField(max_length=10,choices=STATUS_CHOICES)
    facebook_account=models.URLField()
    twitter_account=models.URLField()
    instagram_account=models.URLField()
    linkedin_account=models.URLField()
    target=models.CharField(max_length=200,blank=True,null=True)
    nature_of_assignment=models.CharField(max_length=2000,blank=True,null=True)
    contract_period=models.CharField(max_length=2000,blank=True,null=True)
    final_proposal_amounts=models.CharField(max_length=2000,blank=True,null=True)
    

    def __str__(self):
        return self.client_name

class ContactManager(models.Model):
    STATUS_CHOICES=(
        ('A','Active'),
        ('E','Exited'),
    )
    #personal_details
    contact_name=models.CharField(max_length=250)
    position=models.CharField(max_length=255)
    personal_tel_no=models.CharField(max_length=255)
    personal_email=models.EmailField()
    personal_facebook_account=models.URLField()
    personal_twitter_account=models.URLField()
    personal_instagram_account=models.URLField()
    personal_linkedin_account=models.URLField()
    personal_status=models.CharField(max_length=10,choices=STATUS_CHOICES)
    #office_details
    client=models.ForeignKey(ClientManager,on_delete=models.CASCADE)
    service_line=models.CharField(max_length=250)
    target=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.contact_name

    

class Message(models.Model):
    created_at=models.DateField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateField(auto_now_add=True,blank=True,null=True)
    sms=models.CharField(max_length=4096,blank=True,null=True)
    email_body=models.CharField(max_length=7168,blank=True,null=True)
    email_subject=models.CharField(max_length=1024,blank=True,null=True)
    contacts=models.ManyToManyField(ContactManager,blank=True,help_text="Press ctrl + click to add multiple users")
    clients=models.ManyToManyField(ClientManager,blank=True,help_text="Press ctrl + click to add multiple users")
    account_sid=models.CharField(max_length=1024,null=True,blank=True)
    api_version=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateField(null=True,blank=True)
    date_sent=models.DateField(null=True,blank=True)
    date_updated=models.DateField(null=True,blank=True)
    delete=models.CharField(max_length=1200,null=True,blank=True)
    direction=models.CharField(max_length=1200,null=True,blank=True)
    error_code=models.CharField(max_length=1200,null=True,blank=True)
    error_message=models.CharField(max_length=1200,null=True,blank=True)
    feedback=models.CharField(max_length=1200,null=True,blank=True)
    fetch=models.CharField(max_length=1200,null=True,blank=True)
    from_who=models.CharField(max_length=1200,null=True,blank=True)
    media=models.CharField(max_length=1200,null=True,blank=True)
    messaging_service_sid=models.CharField(max_length=1200,null=True,blank=True)
    num_media=models.CharField(max_length=1200,null=True,blank=True)
    num_segments=models.CharField(max_length=1200,null=True,blank=True)
    price=models.CharField(max_length=1200,null=True,blank=True)
    price_unit=models.CharField(max_length=200,null=True,blank=True)
    sid=models.CharField(max_length=1200,null=True,blank=True)
    status=models.CharField(max_length=1200,null=True,blank=True)
    subresource_uris=models.CharField(max_length=1200,null=True,blank=True)
    to=models.CharField(max_length=1200,null=True,blank=True)
    update=models.CharField(max_length=1200,null=True,blank=True)
    uri=models.CharField(max_length=1200,null=True,blank=True)
    target_sms=models.CharField(max_length=200,null=True,blank=True)
    target_emails=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.sms if self.sms else self.email_subject



class FilterSet(models.Model):
    search_parameter=models.CharField(max_length=2048,null=True,blank=True)
    filtered_list=ArrayField(models.CharField(max_length=2048,null=True,blank=True),null=True,blank=True)
    user_filters=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.id)