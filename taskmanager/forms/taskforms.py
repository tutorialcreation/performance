from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from taskmanager.models import Task,TaskReview,SubTask,Team
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import TabHolder,Tab
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from taskmanager.custom_layout_object import Formset
# Get the user model defined in setting.AUTH_USER_MODEL
UserModel = get_user_model()

class TaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title','assignment_type','assignment_typeset','client_name','assigned_to','due_date','team')

    def __init__(self, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        # import pdb; pdb.set_trace()
        self.helper.layout = Layout(
                Div(
                    Field('title'),
                    Field('client_name'),
                    Field('team'),
                    Field('assigned_to'),
                    Field('assignment_typeset'),
                    Field('assignment_type'),
                    Field('due_date'),
                    Fieldset('Add Task(s)',
                    Formset('subtasks')),
                    HTML("<br>"),
                    ButtonHolder(Submit('submit', 'create task')),
                )
            )
        self.fields["assigned_to"].queryset = Team.objects.none()
        # import pdb; pdb.set_trace()
        if 'team' in self.data:
            try:
                team_id=int(self.data.get('team'))
                self.fields["assigned_to"].queryset=Team.objects.filter(pk=team_id).first().members.all()
            except (ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields["assigned_to"].queryset=Team.objects.all().first().members.all()

        

class TaskUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title','assignment_type','assignment_typeset','client_name','assigned_to','due_date','team')

    def __init__(self, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        # import pdb; pdb.set_trace()
        self.helper.layout = Layout(
                Div(
                    Field('title'),
                    Field('client_name'),
                    Field('team'),
                    # Field('assigned_to'),
                    Field('assignment_typeset'),
                    Field('assignment_type'),
                    Field('due_date'),
                    Fieldset('Add Task(s)',
                    Formset('subtasks')),
                    HTML("<br>"),
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )
        self.fields["assigned_to"].queryset = Team.objects.none()
        self.fields["assignment_typeset"].queryset=Task.objects.none()

        # import pdb; pdb.set_trace()
        if 'team' in self.data:
            try:
                team_id=int(self.data.get('team'))
                self.fields["assigned_to"].queryset=Team.objects.filter(pk=team_id).first().members.all()
            except (ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields["assigned_to"].queryset=Team.objects.all().first().members.all()

        if 'team' in self.data:
            try:
                team_id=int(self.data.get('team'))
                self.fields["assigned_typeset"].queryset=Task.objects.filter(team_id=team_id)
            except (ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields["assigned_to"].queryset=Task.objects.all().first()



class ExtendDeadlineForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('due_date',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ExtendDeadlineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        # import pdb; pdb.set_trace()
        self.helper.layout = Layout(
                Div(
                    Fieldset('Extend Deadline',
                    Formset('subtasks')),
                    HTML("<br>"),
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )
       


class ReassigningForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('due_date',)

    def __init__(self, *args, **kwargs):
        super(ReassigningForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        # import pdb; pdb.set_trace()
        self.helper.layout = Layout(
                Div(
                    Fieldset('Reassign Individual',
                    Formset('subtasks')),
                    HTML("<br>"),
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )
       

class RatingForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('rating','content',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RatingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        # import pdb; pdb.set_trace()
        self.helper.layout = Layout(
                Div(
                    Field('rating'),
                    Field('content'),
                    HTML("<br>"),
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )
        
class SubTaskRatingForm(forms.ModelForm):

    class Meta:
        model = SubTask
        fields = ('rating','content',)

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(SubTaskRatingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        # import pdb; pdb.set_trace()
        self.helper.layout = Layout(
                Div(
                    Field('rating'),
                    Field('content'),
                    HTML("<br>"),
                    ButtonHolder(Submit('submit', 'submit')),
                )
            )
        

class SubTaskForm(forms.ModelForm):

    class Meta:
        model = SubTask
        exclude = ()

SubTaskFormset=inlineformset_factory(Task,SubTask,form=SubTaskForm, fields=['name','member_assigned','task_due_date','prior_task'],extra=1,can_delete=True)

class SubTaskUpdateForm(forms.ModelForm):

    class Meta:
        model = SubTask
        exclude = ()

SubTaskUpdateFormset=inlineformset_factory(Task,SubTask,form=SubTaskUpdateForm, fields=['name','task_due_date'],extra=1,can_delete=True)

class SubTaskReassignForm(forms.ModelForm):

    class Meta:
        model = SubTask
        exclude = ()

SubTaskReassignFormset=inlineformset_factory(Task,SubTask,form=SubTaskUpdateForm, fields=['name','member_assigned'],extra=1,can_delete=True)


class TaskEditForm(ModelForm):

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "w3-input"})
    )

    desc = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={"class": "w3-input", "placeholder": "Describe about task", "rows": 5}
        ),
        required=False
    )

    class Meta:
        model = Task
        fields = ('title', 'desc', 'due_date', 'team', 'assigned_to',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"class": "w3-input", "placeholder": "Enter title for task"}
        )
        self.fields["assigned_to"].widget.attrs.update({"class": "w3-select"})
        self.fields["team"].widget.attrs.update({"class": "w3-select"})
        if kwargs.get('initial').get('has_team'):
            # We don't want user to edit assigned team, if it is already assigned to one team
            del self.fields["team"]
            self.fields["assigned_to"].queryset = kwargs.get('initial').get('members')
        else:
            # If task is still not assigned to any team, there us no need of assigned_to field
            del self.fields["assigned_to"]
            self.fields["team"].queryset = kwargs.get('initial').get('teams')


class SignUpForm(forms.ModelForm):
    """
    A form that creates a user, from the given username, email and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "w3-input", "placeholder": "Make this a good one!"}
        ),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={"class": "w3-input", "placeholder": "Enter same Password, for verification"}
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = UserModel
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "class": "w3-input", "placeholder": "Create a unique username for you!"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "w3-input", "required": True, "placeholder": "Enter your email address"}
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class DateRangeInput(forms.Form):
    date_range_picker=forms.CharField(label='Select Date Range',max_length=1024,required=False)
    multiple_date_picker=forms.CharField(label='Select Multiple Date Range',required=False)

    