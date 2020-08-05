from django.db import models

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


    def __str__(self):
        return self.contact_name

    

