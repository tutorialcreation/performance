from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError

class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self,email):
        RestrictedList=['Your restricted list goes here.']
        if email in RestrictedList:
            raise ValidationError('You are restricted from registering. Please contact admin.')
        return email  



class UsernameMaxAdapter(DefaultAccountAdapter):
    def clean_username(self,username):
        if len(username) > 50:
            raise ValidationError('Please enter a username value less than the current one')
        return DefaultAccountAdapter.clean_username(self,username)