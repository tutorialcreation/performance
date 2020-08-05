from django import forms
from ..models import ClientManager,ContactManager
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper

class ClientForms(forms.ModelForm):
    class Meta:
        model=ClientManager
        fields=[
            'client_name',
            'country',
            'client_tel_no',
            'client_email',
            'client_location',
            'client_postal_address',
            'client_status',
            'facebook_account',
            'twitter_account',
            'instagram_account',
            'linkedin_account',
        ]
    def __init__(self, *args, **kwargs):
        super(ClientForms, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
                Field('client_name'),
                Field('country'),
                Field('client_tel_no'),
                Field('client_email'),
                Field('client_location'),
                Field('client_postal_address'),
                Field('client_status'),
                Field('facebook_account'),
                Field('twitter_account'),
                Field('instagram_account'),
                Field('linkedin_account'),
                Div(
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )


class ContactForms(forms.ModelForm):
    class Meta:
        model=ContactManager
        fields=[
            'contact_name',
            'position',
            'personal_tel_no',
            'personal_email',
            'personal_facebook_account',
            'personal_twitter_account',
            'personal_instagram_account',
            'personal_linkedin_account',
            'personal_status',
            'client',
            'service_line',
        ]

    def __init__(self, *args, **kwargs):
        super(ContactForms, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
                Field('contact_name'),
                Field('position'),
                Field('personal_tel_no'),
                Field('personal_email'),
                Field('personal_facebook_account'),
                Field('personal_twitter_account'),
                Field('personal_instagram_account'),
                Field('personal_linkedin_account'),
                Field('personal_status'),
                Field('client'),
                Field('service_line'),
                Div(
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )
