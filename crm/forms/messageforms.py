from django import forms
from ..models import (
    ClientManager,ContactManager,
    Message,FilterSet
)
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from crispy_forms.helper import FormHelper




class EmailForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=[
            'email_subject',
            'email_body',
        ]

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
                Field('email_body'),
                Field('email_subject'),
                Div(
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )


class SmsForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=[
            'sms',
        ]

    def __init__(self, *args, **kwargs):
        super(SmsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
                Field('sms'),
                Div(
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )



class FilterForm(forms.ModelForm):
    class Meta:
        model=FilterSet
        fields=[
            'search_parameter',
        ]

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
                Field('search_parameter'),
                Div(
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )
