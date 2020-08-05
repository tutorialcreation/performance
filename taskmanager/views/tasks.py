import datetime
import csv, io
import json
import os
import pandas as pd
# import mysql.connector
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q,Avg
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
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
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Func
from django.db import transaction
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from webpush import send_user_notification
from setup import celery_app


from taskmanager.models import Team, Task,SubTask, Comment,Book
from taskmanager.forms.taskforms import (
    TaskCreationForm, 
    TaskEditForm,
    SubTaskForm,
    SubTaskFormset,
    SubTaskUpdateFormset,
    SubTaskReassignFormset,
    TaskUpdateForm,
    ExtendDeadlineForm,
    ReassigningForm,
    RatingForm,
    SubTaskRatingForm,
    DateRangeInput
)
from django.urls import reverse, reverse_lazy



class TaskCreate(CreateView):
    '''
    doc strings should be in every function
    '''
    model = Task
    template_name = 'taskmanager/task_create.html'
    form_class = TaskCreationForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        data = super(TaskCreate, self).get_context_data(**kwargs)
        data['create']=True
        # import pdb; pdb.set_trace()
        if self.request.POST:
            data['subtasks'] = SubTaskFormset(self.request.POST)
        else:
            data['subtasks'] = SubTaskFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        # import pdb; pdb.set_trace()
        subtasks = context['subtasks']
        with transaction.atomic():
            form.instance.creator = self.request.user 
            self.object = form.save()
            if subtasks.is_valid():
                subtasks.instance = self.object
                subtasks.save()
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(BSModalUpdateView):
    model = Task
    template_name = 'taskmanager/task_create-edit.html'
    form_class = ExtendDeadlineForm
    success_message='You have succesfully updated your data.'
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(TaskUpdate, self).get_context_data(**kwargs)
        data['update'] = True
        if self.request.POST:
            # import pdb;pdb.set_trace()
            data['subtasks'] = SubTaskUpdateFormset(self.request.POST, instance=self.object)
        else:
            data['subtasks'] = SubTaskUpdateFormset(instance=self.object)
        return data

    def form_valid(self, form):
        # import pdb; pdb.set_trace()
        context = self.get_context_data()
        subtasks = context['subtasks']
        with transaction.atomic():
            form.instance.creator = self.request.user            
            self.object = form.save()
            if subtasks.is_valid():
                subtasks.instance = self.object
                subtasks.save()
        return super(TaskUpdate, self).form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('taskmanager:task_my_tasks')

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        for item in data:
            if item.startswith("subtask-") and item.endswith("-id") and data[item]:
                id_ = data[item]
                date_key = "subtask-{}-task_due_date".format(item.split("-")[1])
                task_due_date = data[date_key]
                subtask=SubTask.objects.get(pk=id_)
                subtask.task_due_date=task_due_date
                subtask.save()
        return redirect('taskmanager:task_my_tasks')

class Reassigning(UpdateView):
    model = Task
    template_name = 'taskmanager/task_create-edit.html'
    form_class = ReassigningForm
    success_message='You have succesfully updated your data.'
    success_url = reverse_lazy('taskmanager:task_my_tasks')
    # import pdb; pdb.set_trace()

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        data = super(Reassigning, self).get_context_data(**kwargs)
        data['update'] = True
        if self.request.POST:
            # import pdb;pdb.set_trace()
            data['subtasks'] = SubTaskReassignFormset(self.request.POST, instance=self.object)
        else:
            data['subtasks'] = SubTaskReassignFormset(instance=self.object)
        return data

    def form_valid(self, form):
        # import pdb; pdb.set_trace()
        context = self.get_context_data()
        subtasks = context['subtasks']
        with transaction.atomic():
            form.instance.creator = self.request.user 
            # print(form)
            if form.instance.assignment_type == "OTHER":
                form.instance.assignment_type = self.request.POST.get('assignment_specify')                    
           
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
                # import pdb; pdb.set_trace()
                member_assigned = data[member_key]
                subtask=SubTask.objects.get(pk=id_)
                subtask.member_assigned_id=member_assigned
                subtask.save()
        return redirect('taskmanager:task_my_tasks')


class Rating(BSModalUpdateView):
    # specify the model you want to use 
    model = Task 
    template_name = 'taskmanager/task_create-edit.html'
    form_class=RatingForm
    success_message='You have succesfully rated this task.'
  
    success_url = reverse_lazy('taskmanager:task_my_tasks')

    def post(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        form = self.form_class(request.POST)
        # if form.is_valid():
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        subtask_id=request.GET.get('subtask_id')
        subtask=task.subtask.get(pk=subtask_id)
        # import pdb; pdb.set_trace()
        if task.assigned_to.get(username=request.user.username):
            if task.status == 'COMP' or subtask.status == 'RET':
                task.status = 'APP'
                task.rating = request.POST.get('rating')
                task.content= request.POST.get('content')
                task.save()
                messages.success(request, "The task is marked as Approved successfully!")
                # After marking task as completed, redirect user to that task with success message
                return redirect('taskmanager:task_my_tasks')
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

            # return HttpResponseRedirect('/success/')

        return redirect('taskmanager:task_my_tasks')

class SubTaskRating(UpdateView):
    # specify the model you want to use 
    model = Task 
    template_name = 'taskmanager/task_create-edit.html'
    form_class=SubTaskRatingForm
    success_message='You have succesfully rated this task.'
  
    success_url = None

    def post(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        form = self.form_class(request.POST)
        # if form.is_valid():
        subtask_id=request.GET.get('subtask_id')
        # import pdb; pdb.set_trace()
        task = get_object_or_404(Task, id=kwargs.get('pk'))
        subtask=task.subtask.get(pk=subtask_id)
        if task.assigned_to.get(username=request.user.username):
            # import pdb;pdb.set_trace()
            if subtask.status == 'COMP' or subtask.status == 'RET':
                subtask.status = 'APP'
                subtask.approved_date=datetime.datetime.today()
                subtask.rating = request.POST.get('rating')
                subtask.content = request.POST.get('content')
                subtask.save()
                messages.success(request, "The task is marked as Approved successfully!")
                # After marking task as completed, redirect user to that task with success message
                return redirect(reverse('taskmanager:team_detail',kwargs={'team_id':task.team_id}))
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

            # return HttpResponseRedirect('/success/')

        return redirect(reverse('taskmanager:team_detail',kwargs={'team_id':task.team_id}))
    


@login_required
@require_http_methods(["GET", "POST"])
def task_create(request):
    teams = Team.objects.filter(leader=request.user)
    members=User.objects.all()
    if request.method == 'POST':
        subtasks=SubTaskFormset(request.POST)
        # return render(request, template, prompt)
        form = TaskCreationForm(request.POST, initial={'teams': teams})
        # import pdb; pdb.set_trace()
        formset=SubTaskForm(request.POST,extra=2)
        sub_task_list=[]
        member_assigned_list=[]
        if request.POST.get('sub_task_count'):
            formset=SubTaskForm(request.POST,extra=request.POST.get('sub_task_count'))
            field_count=request.POST.get('sub_task_count')
            # sub_task_list=[]
            # print(formset)
            # form=MyForm(request.POST,extra=request.POST.get('sub_task_count'))
            field_count=request.POST.get('sub_task_count')
            member_assigned_list=[]
            for index in range(int(field_count)):
                sub_task_list.append(request.POST.get('sub_task_{}'.format(index)))
                member_assigned_list.append(request.POST.get('member_assigned_sub_task_{}'.format(index)))

        if formset.is_valid():  
            # new_sub_task=formset.save(commit=False)
            # new_sub_task=Task()
            dictionary=dict(zip(sub_task_list,member_assigned_list))
            # task=request.POST.get('task')
            # new_sub_task.sub_tasks=dictionary
            # new_sub_task.desc=task
            # new_sub_task.save()          
            # print(dictionary)
        dictionary=dict(zip(sub_task_list,member_assigned_list))
        if form.is_valid() and formset.is_valid():
            new_task = form.save(commit=False)
            if new_task.assignment_type == "OTHER":
                new_task.assignment_type = request.POST.get('assignment_type_specify')
            task=request.POST.get('task')
            dictionary=dict(zip(sub_task_list,member_assigned_list))
            # import pdb; pdb.set_trace();
            new_task.title=request.POST.get('title')
            new_task.assignment_type=request.POST.get('assignment_type')
            new_task.creator = request.user
            new_task.sub_tasks=dictionary
            new_task.save()
            new_task.desc=task
            # Task is firstly assigned to creator
            new_task.assigned_to.add(request.user)
            messages.success(request, "Task: '{0}' is created successfully!".format(new_task.title))
            # Task is created succesfully, redirect user to new task's detail page
            return redirect(new_task)
        else:
            # Form is not valid, send back with errors
            return render(
                request,
                'taskmanager/task_create-edit.html',
                {'user': request.user, 'form': form, 'formset':formset,'creation': True,'members':members}
            )
    else:
        subtasks=SubTaskFormset()
        form = TaskCreationForm(initial={'teams': teams})
        formset=SubTaskForm()
        return render(
            request,
            'taskmanager/task_create-edit.html',
            {'user': request.user, 'form': form,'formset':formset, 'teams': teams, 'creation': True,'members':members,'subtasks':subtasks}
        )


@login_required
@require_http_methods(["GET", "POST"])
def task_edit(request, task_id):
    """
    Only task creator is able to edit task.
    """
    task = get_object_or_404(Task, id=task_id)
    # Only task creator is allowed to edit task whose status is 'Planned'
    if request.user == task.creator and task.status == 'PLAN':
        teams = Team.objects.filter(leader=request.user)
        has_team = True if task.team else False
        members = task.team.members.all() if has_team else None
        if request.method == 'POST':
            form = TaskEditForm(
                request.POST,
                instance=task,
                initial={'members': members, 'has_team': has_team, 'teams': teams}
            )
            if form.is_valid():
                form.save()
                messages.success(request, "The changes are saved successfully!")
                return redirect(task)
            else:
                # Form is not valid, send back with errors
                return render(
                    request,
                    'taskmanager/task_edit.html',
                    {'user': request.user, 'form': form, 'task': task, 'creation': False}
                )
        else:
            form = TaskEditForm(
                instance=task,
                initial={'members': members, 'has_team': has_team, 'teams': teams}
            )
            return render(
                request,
                'taskmanager/task_edit.html',
                {'user': request.user, 'form': form, 'task': task, 'creation': False}
            )
    else:
        raise PermissionDenied


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
        # After deleting task redirect user to index page with success message
        return redirect('taskmanager:index')
    else:
        # User is not creator of task, raise PermissionDenied
        raise PermissionDenied


@login_required
@require_http_methods(["GET"])
def tasks(request):
    """
    Any authenticated user is able to see incomplete tasks
    created or assigned to him.
    """
    context={}
    context['user'] = request.user
    context['tasks'] = SubTask.objects.filter(Q(status="PLAN") & Q(member_assigned=request.user) )
    context['completed_tasks'] = SubTask.objects.filter(Q(status="COMP") & Q(member_assigned=request.user))
    context['resubmitted_tasks'] = SubTask.objects.filter(Q(status="RET") & Q(member_assigned=request.user))
    context['revised_tasks'] = SubTask.objects.filter(Q(status="REV") & Q(member_assigned=request.user))
    context['approved_tasks'] = SubTask.objects.filter(Q(status="APP") & Q(member_assigned=request.user))
    context['pending_approval'] = SubTask.objects.filter(Q(status="PA") & Q(member_assigned=request.user))
    context['tasks_inprogress'] = SubTask.objects.filter(Q(status="PROG") & Q(member_assigned=request.user))
    context['taskset'] = Task.objects.filter(Q(assigned_to=request.user))
    context['completed_tasks']=[*context['completed_tasks'],*context['resubmitted_tasks'],*context['pending_approval']]
    context['completed_or_approved_tasks'] = [*context['completed_tasks'],*context['approved_tasks'],
    *context['revised_tasks'],]
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
    context['team']  = get_object_or_404(Team, id=team_id)
    context['tasks'] = context['team'].task_set.filter(subtask__status="PLAN")
    context['completed_tasks'] = context['team'].task_set.filter(subtask__status="COMP")
    context['resubmitted_tasks'] = context['team'].task_set.filter(subtask__status="RET")
    context['revised_tasks'] = context['team'].task_set.filter(subtask__status="REV")
    context['approved_tasks'] =context['team'].task_set.filter(subtask__status="APP")

    # import pdb;pdb.set_trace()
    context['tasks_inprogress'] =context['team'].task_set.filter(subtask__status="PROG")
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
def completed_tasks(request):
    """
    Any authenticated user is able to see completed tasks
    created or assigned to him.
    """
    tasks = Task.objects.filter(
        Q(creator=request.user) | Q(assigned_to=request.user)
    ).filter(status="COMP").distinct()
    return render(
        request,
        'taskmanager/tasks.html',
        {'user': request.user, 'completed_tasks': tasks, 'completed': True}
    )




@login_required
@require_http_methods(["GET"])
def task_detail(request, task_id):
    """
    Only task creator and members of task's team can see details of task.
    """
    task = get_object_or_404(Task, id=task_id)
    subtasks=task.subtask.all()
    my_subtasks=task.subtask.filter(member_assigned=request.user)
    
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
            {'user': request.user, 'task': task,'subtasks':subtasks,'my_subtasks':my_subtasks}
        )
    else:
        raise PermissionDenied


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
        # import pdb;pdb.set_trace()
        if subtask.status == 'PLAN':
            subtask.status = 'PROG'
            task.status = 'PROG'
            subtask.accepted_date = datetime.date.today()
            subtask.accepted_by = request.user
            subtask.save()
            task.save()
            messages.success(request, "The task has been marked as ongoing successfully!")
            # After marking task as In-Progress, redirect user to that task with success message
            return redirect('taskmanager:task_my_tasks')
        else:
            raise PermissionDenied
    else:
        if subtask.status == 'PLAN':
            subtask.status = 'PA'
            subtask.accepted_by=request.user
            subtask.save()
            messages.success(request,"The task has been marked as pending approval successfully")
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
            subtask.accepted_date = datetime.date.today()
            subtask.accepted_by = request.user
            subtask.save()
            messages.success(request, "The task has been marked as ongoing successfully!")
            # After marking task as In-Progress, redirect user to that task with success message
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
    # subtask=task.subtask.get(if)
    subtask_id=request.GET.get('subtask_id')
    subtask=task.subtask.get(pk=subtask_id)
    # subtasks_completed=task.subtask.filter(status='COMP').count()
    # subtasks_total=task.subtask.all()

    if request.user == task.creator or request.user in task.team.members.all():
        if subtask.status == 'PROG' or task.status == 'PROG':
            if task.task_count == 100:
                task.status='COMP'
                task.save()
            subtask.status = 'COMP'
            subtask.completed_date = datetime.date.today()
            subtask.save()
            messages.success(request, "The task is marked as Completed successfully!")
            # After marking task as completed, redirect user to that task with success message
            return redirect('taskmanager:task_my_tasks')
        elif subtask.status=='REV':
            subtask.status = 'RET'
            subtask.revised_due_date = datetime.date.today()
            subtask.save()
            messages.success(request, "The task is marked as Completed successfully!")
            # After marking task as completed, redirect user to that task with success message
            return redirect('taskmanager:task_my_tasks')
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied

@login_required
@require_http_methods(["GET"])
def task_mark_approved(request, task_id):
    """
    Only task creator and assigned users can mark task as Completed.
    """
    task = get_object_or_404(Task, id=task_id)
    subtask_id=request.GET.get('subtask_id')
    subtask=task.subtask.get(pk=subtask_id)
    if request.user == task.creator or request.user in task.team.members.all():
        if subtask.status == 'COMP':
            subtask.status = 'APP'
            subtask.approved_date = datetime.date.today()
            subtask.save()
            messages.success(request, "The task is marked as Completed successfully!")
            # After marking task as completed, redirect user to that task with success message
            return redirect('taskmanager:task_my_tasks')
        elif subtask.status == 'RET':
            subtask.status = 'APP'
            subtask.completed_date = datetime.date.today()
            subtask.save()
            messages.success(request, "The task is marked as Completed successfully!")
            # After marking task as completed, redirect user to that task with success message
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
            messages.success(request,'The task has been approved you can begin working on the task.')
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
    if request.user == task.creator or request.user in task.team.members.all():
        if subtask.status == 'PROG' or subtask.status=='COMP':
            subtask.status = 'REV'
            subtask.completed_date = datetime.date.today()
            subtask.save()
            messages.success(request, "The task is marked as Completed successfully!")
            # After marking task as completed, redirect user to that task with success message
            return redirect('taskmanager:task_my_tasks')
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
    if request.user == task.creator or request.user:
        allowed = True
    elif task.team:
        if request.user in task.team.members.all():
            allowed = True
        else:
            allowed = False
    else:
        allowed = False
    # If user is allowed to comment, add comment else raise PermissionDenied
    if allowed:
        if request.POST.get('comment_body').strip():
            comment = Comment(
                author=request.user,
                task=task,
                body=request.POST['comment_body']
            )
            comment.save()
            messages.success(request, "The comment is added succesfully")
            # After adding the comment, redirect user to that task with success message
            return redirect(task)
        else:
            messages.error(request, "Missing required fields")
            return redirect(task)
    else:
        raise PermissionDenied


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "You are inputing incorrect format Martin"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occured"})


@require_GET
def view_push(request):
    context = {}
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    context['vapid_key'] = webpush_settings.get('VAPID_PUBLIC_KEY')
    context['user'] = request.user
    return render(request, 'taskmanager/push_requests.html', context)






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


