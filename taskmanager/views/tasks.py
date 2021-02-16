import datetime
import csv, io
import json
import os
import pandas as pd
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q,Avg
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Func
from django.db import transaction
from notifications.models import Notification
from notifications.signals import notify
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from webpush import send_user_notification
from setup import celery_app


from taskmanager.models.tasks import (
    Team,
    Task,
    SubTask,
    InvoiceDetail,
    Comment,
    Book,
    NotificationSet,
    TaskSource,
    BiddedTask,
    BidOrAwardAnalyzer
)

from taskmanager.forms.taskforms import (
    TaskCreationForm, 
    TaskEditForm,
    SubTaskForm,
    SubTaskExtendForm,
    SubTaskFormset,
    SubTaskUpdateFormset,
    SubTaskExtendFormset,
    SubTaskReassignFormset,
    TaskUpdateForm,
    ExtendDeadlineForm,
    ReassigningForm,
    RatingForm,
    SubTaskRatingForm,
    DateRangeInput,
    ReturnForm,
    SuccessForm,
    TaskSourceForm,
    TaskBidForm,
    SubTaskBidForm,
    SubTaskBidFormset,
    InvoicingForm
)
from django.urls import reverse, reverse_lazy




class TaskCreate(CreateView):
    '''
    this task creation has formsets.
    '''
    model = Task
    template_name = 'taskmanager/task_create.html'
    form_class = TaskCreationForm
    success_message='You have successfully created a project. Thank you'
    success_url = '.'


    def get_context_data(self, **kwargs):
        data = super(TaskCreate, self).get_context_data(**kwargs)
        data['create']=True
        if self.request.POST:
            data['subtasks'] = SubTaskFormset(self.request.POST)
        else:
            data['subtasks'] = SubTaskFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        subtasks = context['subtasks']
        with transaction.atomic():
            form.instance.creator = self.request.user 
            self.object = form.save()
            if subtasks.is_valid():
                subtasks.instance = self.object
                # import pdb;pdb.set_trace()
                subtasks.save()

                subject = f'Task Notification'
                tasks_send=[]
                subs=subtasks.instance.subtask.filter(member_assigned=self.request.user)
                site=self.request.build_absolute_uri('/task-master/my-tasks/')
                for task in range(len(subs)):
                    tasks_send.append(subs[task].name)
                message = f'You have received the tasks: {tasks_send} ' \
                          f';from the project {subtasks.instance.title} kindly check the system to view which task you have been allocated.' \
                          f' go to site {site}'
                # notification=NotificationSet.objects.filter(user=self.request.user).first()
                # # import pdb;pdb.set_trace()
                all_subtasks=subtasks.instance.subtask.all()
                target_emails=[]
                target_users=[]
                for data in all_subtasks:
                    target_emails.append(data.member_assigned.email)
                    target_users.append(data.member_assigned)
                notify.send(self.request.user,recipient=target_users,verb=f"You have received a new task from the project {subtasks.instance.title}")
                send_mail(subject,message,settings.FROM_EMAIL,target_emails)
        return super(TaskCreate, self).form_valid(form)


class TaskBidCreate(CreateView):
    '''
    this task creation has formsets.
    '''
    model = BiddedTask
    template_name = 'taskmanager/task_create_edit.html'
    form_class = TaskBidForm
    success_message='You have succesfully extended the deadline. Thank you'
    success_url = reverse_lazy('taskmanager:task_my_tasks')

    def get_context_data(self, **kwargs):
        data = super(TaskBidCreate, self).get_context_data(**kwargs)
        data['bidding'] = True
        if self.request.POST:
            data['bids'] = SubTaskBidFormset(self.request.POST, instance=self.object)
        else:
            data['bids'] = SubTaskBidFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        subtasks = context['bids']
        with transaction.atomic():
            form.instance.creator = self.request.user 
            self.object = form.save()
            if subtasks.is_valid():
                subtasks.instance = self.object
                subtasks.save()
        return super(TaskBidCreate, self).form_valid(form)


class TaskUpdate(BSModalUpdateView):
    model = Task
    template_name = 'taskmanager/task_create_edit.html'
    form_class = TaskUpdateForm
    success_message='You have succesfully updated the project. Thank you'
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(TaskUpdate, self).get_context_data(**kwargs)
        data['update'] = True
        if self.request.POST:
            data['subtasks'] = SubTaskUpdateFormset(self.request.POST, instance=self.object)
        else:
            data['subtasks'] = SubTaskUpdateFormset(instance=self.object)
        return data

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        task_id=kwargs.get('pk')
        task=Task.objects.get(id=task_id)
        task.title=request.POST.get('title')
        assignment_typeset=Task.objects.get(id=request.POST.get('assignment_typeset'))
        task.assignment_typeset=assignment_typeset
        teams=Team.objects.get(id=request.POST.get('team'))
        task.team=teams
        task.client_name=request.POST.get('client_name')
        task.due_date=request.POST.get('due_date')
        task.save()
        for item in data:
            if item.startswith("subtask-") and item.endswith("-id") and data[item]:
                id_ = data[item]
                date_key = "subtask-{}-task_due_date".format(item.split("-")[1])
                member_key="subtask-{}-member_assigned".format(item.split("-")[1])
                task_due_date = data[date_key]
                member_assigned=data[member_key]
                member_assigned=User.objects.get(id=member_assigned)
                subtask=SubTask.objects.get(pk=id_)
                subtask.task_due_date=task_due_date
                subtask.member_assigned=member_assigned
                subtask.save()
        return redirect('taskmanager:task_my_tasks')


@login_required
@require_http_methods(["GET","POST"])
def task_detail(request, task_id):
    """
    Only task creator and members of task's team can see details of task.
    """
    task = get_object_or_404(Task, id=task_id)
    subtasks=task.subtask.all()
    my_subtasks=task.subtask.filter(member_assigned=request.user)
    form=SuccessForm()
    context={}
    if request.method=='POST':
        success=request.POST.get('was_the_bid_successful')
        print(request.POST)
        print(request.POST.get('task_info'))
        if success=='SUCCESS':
            if task.status=='PLAN' or task.status=='PROG' or task.status=='NBID':
                task.status='BID'
                task.save()
        else:
            if task.status=='PLAN' or task.status=='PROG':
                task.status='NBID'
                task.notification_date=request.POST.get('notification_date')
                task.unsuccess_reason=request.POST.get('unsuccessful_reason')
                task.save()
                return redirect('taskmanager:task_create')
            
        print(success)
    # task_review = Task.objects.get(status='COMP').annotate(avg_review=Round(Avg('rating')))
    if request.user == task.creator or request.user in task.assigned_to.all():
        allowed = True
    elif task.team:
        if request.user in task.team.members.all():
            allowed = True
        else:
            allowed = False
    else:
        allowed = False
    # If user is allowed to see details return details else raise PermissionDenied
    if allowed:
        return render(
            request,
            'taskmanager/task_detail.html',
            {'user': request.user, 'task': task,'subtasks':subtasks,'my_subtasks':my_subtasks,'success_form':form}
        )
    else:
        raise PermissionDenied




class ExtendDeadline(BSModalUpdateView):
    model = Task
    template_name = 'taskmanager/task_create_edit.html'
    form_class = ExtendDeadlineForm
    success_message='You have succesfully extended the deadline. Thank you'
    success_url = reverse_lazy('taskmanager:task_my_tasks')

    def get_context_data(self, **kwargs):
        data = super(ExtendDeadline, self).get_context_data(**kwargs)
        data['update'] = True
        if self.request.POST:
            data['subtasks'] = SubTaskExtendFormset(self.request.POST, instance=self.object)
        else:
            data['subtasks'] = SubTaskExtendFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        subtasks = context['subtasks']
        with transaction.atomic():
            form.instance.creator = self.request.user 
            self.object = form.save()
            if subtasks.is_valid():
                subtasks.instance = self.object
                subtasks.save()
        return super(ExtendDeadline, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        for item in data:
            if item.startswith("subtask-") and item.endswith("-id") and data[item]:
                id_ = data[item]
                date_key = "subtask-{}-task_due_date".format(item.split("-")[1])
                reason_key="subtask-{}-extension_reason".format(item.split("-")[1])
                task_due_date = data[date_key]
                extension_reason=data[reason_key]
                subtask=SubTask.objects.get(pk=id_)
                subtask.extension_reason=extension_reason
                subtask.task_due_date=task_due_date
                # import pdb;pdb.set_trace()
                subtask.save()
        return redirect('taskmanager:task_my_tasks')


class TaskBid(BSModalUpdateView):
    model = BiddedTask
    template_name = 'taskmanager/task_create_edit.html'
    form_class = TaskBidForm
    success_message='You have succesfully extended the deadline. Thank you'
    success_url = reverse_lazy('taskmanager:task_my_tasks')

    def get_context_data(self, **kwargs):
        data = super(TaskBid, self).get_context_data(**kwargs)
        data['bidding'] = True
        if self.request.POST:
            data['bids'] = SubTaskBidFormset(self.request.POST, instance=self.object)
        else:
            data['bids'] = SubTaskBidFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        subtasks = context['bids']
        with transaction.atomic():
            form.instance.creator = self.request.user 
            self.object = form.save()
            if subtasks.is_valid():
                subtasks.instance = self.object
                subtasks.save()
        return super(TaskBid, self).form_valid(form)

class RequestInvoice(CreateView):
    model = InvoiceDetail
    template_name = 'taskmanager/task_create_edit.html'
    form_class = InvoicingForm
    success_message='You have succesfully requested for an invoice. Thank you'
    success_url = reverse_lazy('taskmanager:task_my_tasks')

    def get_context_data(self, **kwargs):
        data = super(RequestInvoice, self).get_context_data(**kwargs)
        data['invoice'] = True
        return data

    def form_valid(self, form):
        with transaction.atomic():
            if form.is_valid():
                form.instance.project_id=self.request.GET.get('task')
                form.instance.is_invoiced=True
                form.save()
        return super(RequestInvoice, self).form_valid(form)


class Reassigning(BSModalUpdateView):
    model = Task
    template_name = 'taskmanager/task_create_edit.html'
    form_class = ReassigningForm
    success_message='You have succesfully reassigned the assignment to another individual. Thank you'
    success_url = reverse_lazy('taskmanager:task_my_tasks')

    def get_context_data(self, **kwargs):
        data = super(Reassigning, self).get_context_data(**kwargs)
        data['update'] = True
        if self.request.POST:
            data['subtasks'] = SubTaskReassignFormset(self.request.POST, instance=self.object)
        else:
            data['subtasks'] = SubTaskReassignFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        subtasks = context['subtasks']
        with transaction.atomic():
            form.instance.creator = self.request.user 
            self.object = form.save()
            if subtasks.is_valid():
                subtasks.instance = self.object
                subtasks.save()
        return super(Reassigning, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        for item in data:
            if item.startswith("subtask-") and item.endswith("-id") and data[item]:
                id_ = data[item]
                member_key = "subtask-{}-member_assigned".format(item.split("-")[1])
                reason_key="subtask-{}-reassign_reason".format(item.split("-")[1])
                member_assigned = data[member_key]
                reassign_reason=data[reason_key]
                subtask=SubTask.objects.get(pk=id_)
                subtask.reassign_reason=reassign_reason
                subtask.member_assigned_id=member_assigned
                subtask.save()
        return redirect('taskmanager:task_my_tasks')



class Revision(BSModalUpdateView):
    model = Task
    template_name = 'taskmanager/task_create_edit.html'
    form_class = ReturnForm
    success_url = reverse_lazy('taskmanager:task_my_tasks')

    def get_context_data(self, **kwargs):
        context = super(Revision, self).get_context_data(**kwargs)
        context['revision'] = True
        return context

    def post(self, request, *args, **kwargs):
        subtask_id=request.GET.get('subtask_id')
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        subtask=task.subtask.get(pk=subtask_id)
        if task.assigned_to.get(username=request.user.username):
            if subtask.status == 'RET' or subtask.status=='COMP':
                subtask.status = 'REV'
                subtask.return_reason=request.POST.get('return_reason')
                subtask.save()
                messages.success(request, f"The task {subtask.name} has been returned for revision")
                return redirect(reverse('taskmanager:team_detail',kwargs={'team_id':task.team_id}))
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

class Rating(BSModalUpdateView):
    model = Task 
    template_name='taskmanager/task_create-edit.html'
    form_class=RatingForm
    success_message='You have succesfully rated this project. thank you'
    success_url=None

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        if task.assigned_to.get(username=request.user.username):
            if task.status == 'COMP':
                task.status = 'APP'
                task.rating = request.POST.get('rating')
                task.content= request.POST.get('content')
                task.save()
                return redirect('taskmanager:task_my_tasks')
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

            
        return redirect('taskmanager:task_my_tasks')

class SubTaskRating(BSModalUpdateView): 
    model = Task 
    template_name = 'taskmanager/task_create_edit.html'
    form_class=SubTaskRatingForm
    success_message='You have succesfully rated this assignment. thank you'  
    success_url = None

    def post(self, request, *args, **kwargs):
        subtask_id=request.GET.get('subtask_id')
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        subtask=task.subtask.get(pk=subtask_id)
        if task.assigned_to.get(username=request.user.username):
            if subtask.status == 'COMP' or subtask.status == 'RET':
                subtask.status = 'APP'
                subtask.approved_date=datetime.datetime.today()
                subtask.rating = request.POST.get('rating')
                subtask.content = request.POST.get('content')
                subtask.save()
                return redirect(reverse('taskmanager:team_detail',kwargs={'team_id':task.team_id}))
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied


        return redirect(reverse('taskmanager:team_detail',kwargs={'team_id':task.team_id}))
    






@login_required
@require_http_methods(["GET"])
def task_delete(request, task_id):
    """
    Only task creator can delete task if task is IN-PROGRESS.
    """
    task = get_object_or_404(Task, id=task_id)
    if request.user == task.creator and task.status == 'PLAN':
        task.delete()
        messages.success(request, "The task is deleted successfully!")
        return redirect('taskmanager:index')
    else:
        raise PermissionDenied


@login_required
@require_http_methods(['GET'])
def subtask_delete(request,subtask_id):
    subtask=get_object_or_404(SubTask,id=subtask_id)
    if subtask.task.assigned_to.get(username=request.user.username) and subtask.status=='PLAN':
            subtask.delete()
            messages.success(request,'You have successfully deleted the assignment. thank you')
            return redirect('taskmanager:task_my_tasks')
    else:
        raise PermissionDenied


@login_required
@require_http_methods(["GET","POST"])
def tasks(request):
    """
    Any authenticated user is able to see incomplete tasks
    created or assigned to him.
    """
    # requests.get('/inbox/notifications/api/unread_list/?mark_as_read=true', params=request.GET)
    context={}
    context['user'] = request.user
    context['tasks'] = SubTask.objects.filter(Q(status="PLAN") & Q(member_assigned=request.user) )
    context['completed_tasks'] = SubTask.objects.filter(Q(status="COMP") & Q(member_assigned=request.user))
    context['resubmitted_tasks'] = SubTask.objects.filter(Q(status="RET") & Q(member_assigned=request.user))
    context['revised_tasks'] = SubTask.objects.filter(Q(status="REV") & Q(member_assigned=request.user))
    context['approved_tasks'] = SubTask.objects.filter(Q(status="APP") & Q(member_assigned=request.user))
    context['invoiced_tasks']=SubTask.objects.filter(Q(status='INV') & Q(member_assigned=request.user))
    context['pending_approval'] = SubTask.objects.filter(Q(status="PA") & Q(member_assigned=request.user))
    context['tasks_inprogress'] = SubTask.objects.filter(Q(status="PROG") & Q(member_assigned=request.user))
    context['taskset'] = Task.objects.filter(Q(assigned_to=request.user))
    context['successful_bids']= Task.objects.filter(Q(status="BID"))
    context['unsuccessful_bids']= Task.objects.filter(Q(status="NBID"))
    context['completed_tasks']=[*context['completed_tasks'],*context['resubmitted_tasks'],*context['pending_approval']]
    context['completed_or_approved_tasks'] = [*context['completed_tasks'],*context['approved_tasks'],
    *context['revised_tasks'],*context['invoiced_tasks']]
    context['tasks_inprogress']=[*context['tasks_inprogress'],*context['revised_tasks']]
    return render(
        request,
        'taskmanager/tasks.html',
        context
    )


@login_required
@require_http_methods(["GET"])
def team_tasks(request,team_id):
    """
    Any authenticated user is able to see incomplete tasks
    created or assigned to him.
    """
    context={}
    context['user'] = request.user
    team=get_object_or_404(Team,id=team_id)
    context['team']  = team
    context['tasks'] = team.task_set.filter(subtask__status="PLAN")
    context['completed_tasks'] = team.task_set.filter(subtask__status="COMP")
    context['resubmitted_tasks'] = team.task_set.filter(subtask__status="RET")
    context['revised_tasks'] = team.task_set.filter(subtask__status="REV")
    context['approved_tasks'] = team.task_set.filter(subtask__status="APP")
    context['tasks_inprogress'] = team.task_set.filter(subtask__status="PROG")
    context['completed_tasks']=[*context['completed_tasks'],*context['resubmitted_tasks']]
    context['completed_or_approved_tasks'] = [*context['completed_tasks'],*context['approved_tasks'],*context['revised_tasks']]
    context['tasks_inprogress']=[*context['tasks_inprogress'],*context['revised_tasks']]
    return render(
        request,
        'taskmanager/team_tasks.html',
        context
    )


@login_required
@require_http_methods(["GET"])
def task_accept(request, task_id):
    """
    Only assigned users can accept task and mark as In-Progress.
    """
    task = get_object_or_404(Task, id=task_id)
    subtask_id=request.GET.get('subtask_id')
    subtask=task.subtask.get(pk=subtask_id)
    if request.user in task.team.members.all():
        if subtask.status == 'PLAN':
            subtask.status = 'PROG'
            task.status = 'PROG'
            subtask.accepted_date = datetime.date.today()
            subtask.accepted_by = request.user
            subtask.save()
            task.save()
            messages.success(request, 'The task has been marked as accepted successfully. Thank you')
            return redirect('taskmanager:task_my_tasks')
        else:
            raise PermissionDenied
    else:
        if subtask.status == 'PLAN':
            subtask.status = 'PA'
            subtask.accepted_by=request.user
            subtask.save()
            messages.success(request,'The task is waiting for approval for you to begin because this task is from an external team. thank you')
            return redirect('taskmanager:task_my_tasks')
        raise PermissionDenied

@login_required
@require_http_methods(["GET"])
def task_resubmit(request, task_id):
    """
    Only assigned users can accept task and mark as In-Progress.
    """
    task = get_object_or_404(Task, id=task_id)
    subtask_id=request.GET.get('subtask_id')
    subtask=task.subtask.get(pk=subtask_id)
    if request.user in task.team.members.all():
        if subtask.status == 'REV':
            subtask.status = 'RES'
            subtask.save()
            messages.success(request, "The task has been successfully resubmitted. Thank you!")
            return redirect('taskmanager:task_my_tasks')
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


@login_required
@require_http_methods(["GET"])
def task_mark_completed(request, task_id):
    """
    Only task creator and assigned users can mark task as Completed.
    """
    task = get_object_or_404(Task, id=task_id)
    subtask_id=request.GET.get('subtask_id')
    subtask=task.subtask.get(pk=subtask_id)
    
    if request.user == task.creator or request.user in task.team.members.all():
        if subtask.status == 'PROG' or task.status == 'PROG':
            if task.task_count == 100:
                task.status='COMP'
                task.completed_date=datetime.datetime.today()
                task.save()
                messages.success(request, "The project has been successfully marked as completed. Thank you!")
            subtask.status = 'COMP'
            subtask.completed_date = datetime.date.today()
            subtask.save()
            site=request.build_absolute_uri('/task-master/my-tasks/')
            subject = f'Task Notification'
            message = f'The task {subtask.name} has been completed . And is ready for review go to site {site}'
            target_email=[task.assigned_to.first().email]
            send_mail(subject,message,settings.FROM_EMAIL,target_email)
            messages.success(request, "The task has been successfully marked as completed. Thank you!")
            return redirect('taskmanager:task_my_tasks')
        elif subtask.status=='REV':
            subtask.status = 'RET'
            subtask.revised_due_date = datetime.datetime.today()
            subtask.save()
            messages.success(request, "The task has been successfully resubmited. Thank you!")
            return redirect('taskmanager:task_my_tasks')
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

@login_required
@require_http_methods(["GET"])
def task_mark_pending_approved(request,task_id):
    task=get_object_or_404(Task,id=task_id)
    subtask_id=request.GET.get('subtask_id')
    subtask=task.subtask.get(pk=subtask_id)
    if request.user:
        if subtask.status == 'PA':
            subtask.status = 'PROG'
            subtask.save()
            messages.success(request,f"The assignment {subtask.name} has been approved and you can begin working on it. Thank you!")
            return redirect('taskmanager:task_my_tasks')
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

@login_required
@require_http_methods(["GET"])
def task_mark_revision(request, task_id):
    """
    Only task creator and assigned users can mark task as Completed.
    """
    task = get_object_or_404(Task, id=task_id)
    subtask_id=request.GET.get('subtask_id')
    subtask=task.subtask.get(pk=subtask_id)
    if task.assigned_to.get(username=request.user.username) or request.method=='POST':
        if subtask.status == 'RET' or subtask.status=='COMP':
            subtask.status = 'REV'
            subtask.return_reason=request.POST.get('return_reason')
            subtask.save()
            messages.success(request, f"The task {subtask.name} has been returned for revision")
            return redirect(reverse('taskmanager:team_detail',kwargs={'team_id':task.team_id}))
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


@login_required
@require_http_methods(["POST"])
def task_comment(request, task_id):
    """
    Only task creator, assigned users and members of task's team can comment on task.
    """
    task = get_object_or_404(Task, id=task_id)
    if request.user == task.creator:
        allowed = True
    elif task.team:
        if request.user in task.team.members.all():
            allowed = True
        else:
            allowed = False
    else:
        allowed = False
    
    if allowed:
        if request.POST.get('comment_body').strip():
            comment = Comment(
                author=request.user,
                task=task,
                body=request.POST['comment_body']
            )
            comment.save()
            messages.success(request, "The comment is added succesfully")
            return redirect(task)
        else:
            messages.error(request, "Missing required fields")
            return redirect(task)
    else:
        raise PermissionDenied






def load_members(request):
    team_id = request.GET.get('team')
    members = Team.objects.filter(pk=team_id).first().members.all()
    return render(request, 'taskmanager/team_dropdown.html', {
        'members': members,
        'load_members':True
        })
        

def load_projects(request):
    team_id = request.GET.get('teamset')
    assignment_typeset=Task.objects.filter(team_id=team_id)
    return render(request, 'taskmanager/team_dropdown.html', {
        'assignment_typeset':assignment_typeset,
        'load_projects':True
        })



def task_sources(request):
    form=TaskSourceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Project source has been successfully recorded')
        
        context={'form':form}
        return render(request,'taskmanager/task_source.html',context)
    else:
        form=TaskSourceForm()
        context={'form':form}
        return render(request,'taskmanager/task_source.html',context)



