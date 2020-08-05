from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,JsonResponse
from taskmanager.models.tasks import Team
from taskmanager.forms.taskforms import DateRangeInput
from taskmanager.models.tasks import Task,Team,TaskAnalysis,SubTaskAnalysis,SubTask
from django.db.models import Avg,Q,Sum,Max,Count
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.style as mplstyle
import mplcursors
import pandas as pd
import numpy as np
import math
import io
import calendar
import urllib,base64

def split_dates(data):
    splitted_data=data.split()
    splitted_data.remove('-')
    return splitted_data

def to_datetime(data):
    converted_date = datetime.strptime(data, "%m/%d/%Y")
    return converted_date

def myplotter(ax,data1,data2,param_dict):
    mplstyle.use([ 'ggplot', 'fast'])
    formatter = mdates.DateFormatter("%Y-%m-%d")
    # ax.xaxis.set_major_formatter(formatter)
    # locator = mdates.DayLocator()
    # ax.xaxis.set_major_locator(locator)
    out=ax.plot(data1,data2,**param_dict)
    ax.set_ylabel('Scores')
    ax.set_xlabel('Time in Months')
    # ax.set_xlim([datetime(2020, 1, 1), datetime(2020, 1, 31)])
    # ax.set_xlim([0,5])
    # ax.set_facecolor('mediumseagreen')
    ax.legend()
    return out

def index(request):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,figsize=(10,4))
    subtasks=SubTask.objects.filter(member_assigned=request.user)
    deadline=[]
    deadline_score=[]
    resubmission_score=[]
    reset_score=[]
    quality_score=[]
    
    for subtask in subtasks:
        deadline_score.append(subtask.subtask_deadline_score)
        resubmission_score.append(subtask.subtask_resubmission_score)
        reset_score.append(subtask.subtask_deadline_reset_score)
        quality_score.append(subtask.rating)
        deadline.append(subtask.task_due_date.timestamp())
    myplotter(ax1,deadline,deadline_score,{'marker':'x','label':'deadline'})
    ax1.set_title('deadline score')
    myplotter(ax2,deadline,resubmission_score,{'marker':'o','label':'resubmission'})
    ax2.set_title('resubmission score')
    myplotter(ax3,deadline,reset_score,{'marker':'x','label':'reset'})
    ax3.set_title('deadline reset score')
    myplotter(ax4,deadline,quality_score,{'marker':'o','label':'quality'})
    ax4.set_title('quality score')
    
    # mplcursors.cursor(hover=True)
    # crs = mplcursors.cursor(ax1,hover=True)
    # crs.connect("add", lambda sel: sel.annotation.set_text(
    # 'Point {},{}'.format(sel.target[0], sel.target[1])))
    fig=plt.gcf()
    buf=io.BytesIO()
    # mplcursors.cursor(hover=True)
    fig.tight_layout(pad=2.0)
    fig.savefig(buf,format='png')
    buf.seek(0)
    string=base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    
    if request.user is not None:
        projects_incharge=Task.objects.filter(assigned_to=request.user)
        projects_completed=Task.objects.filter(Q(assigned_to=request.user) & Q(subtask__status='COMP'))
        subtasks=SubTask.objects.filter(member_assigned=request.user)
    if request.method == 'POST':
        form = DateRangeInput(request.POST or None)
        if form.is_valid():
            date_range=form.cleaned_data.get('date_range_picker')
            splitted_dates = split_dates(date_range)
            start_date= to_datetime(splitted_dates[0])
            end_date=to_datetime(splitted_dates[1])
            project_sets = TaskAnalysis.objects.filter(Q(revised_due_date__gte=start_date) & Q(revised_due_date__lte=end_date))
            project_set = Task.objects.filter(Q(completed_date__gte=start_date) & Q(completed_date__lte=end_date))
            subtask_sets = SubTaskAnalysis.objects.filter(Q(revised_due_date__gte=start_date) & Q(revised_due_date__lte=end_date))
            subtask_set = SubTask.objects.filter(Q(completed_date__gte=start_date) & Q(completed_date__lte=end_date))
            project_sets = [*project_sets,*project_set,*subtask_sets,*subtask_set]
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,figsize=(10,4))
            if form.cleaned_data.get('date_range_picker') and not form.cleaned_data.get('multiple_date_picker'):
                subtasks=SubTask.objects.filter(Q(task_due_date__gte=start_date) & Q(task_due_date__lte=end_date) & Q(member_assigned=request.user))
            else:
                multiple_dates=form.cleaned_data.get('multiple_date_picker').split(',')
                multiple_value_dates=[datetime.strptime(data,"%m/%d/%Y") for data in multiple_dates]
                subtasks=SubTask.objects.filter(Q(task_due_date__in=multiple_value_dates) & Q(member_assigned=request.user))
            deadline=[]
            deadline_score=[]
            resubmission_score=[]
            reset_score=[]
            quality_score=[]
            for subtask in subtasks:
                deadline_score.append(subtask.subtask_deadline_score)
                resubmission_score.append(subtask.subtask_resubmission_score)
                reset_score.append(subtask.subtask_deadline_reset_score)
                quality_score.append(subtask.rating)
                deadline.append(subtask.task_due_date.timestamp())
            myplotter(ax1,deadline,deadline_score,{'marker':'x','label':'deadline'})
            ax1.set_title('deadline score')
            myplotter(ax2,deadline,resubmission_score,{'marker':'o','label':'resubmission'})
            ax2.set_title('resubmission score')
            myplotter(ax3,deadline,reset_score,{'marker':'x','label':'reset'})
            ax3.set_title('deadline reset score')
            myplotter(ax4,deadline,quality_score,{'marker':'o','label':'quality'})
            ax4.set_title('quality score')
            # crs = mplcursors.cursor(ax1,hover=True)
            # crs.connect("add", lambda sel: sel.annotation.set_text(
            # 'Point {},{}'.format(sel.target[0], sel.target[1])))
            # mplcursors.cursor(hover=True)
            fig=plt.gcf()
            buf=io.BytesIO()
            # mplcursors.cursor(hover=True)
            fig.tight_layout(pad=2.0)
            fig.savefig(buf,format='png')
            buf.seek(0)
            string=base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            projects_incharge=Task.objects.filter(assigned_to=request.user)
            projects_completed=Task.objects.filter(Q(assigned_to=request.user) & Q(subtask__status='COMP'))
            subtasks=SubTask.objects.filter(member_assigned=request.user)
            return render(request,'_layout.html',{'form':form,'project_sets':project_sets,'date_range':date_range,'data':uri,
            'subtasks':subtasks,'projects_incharge':projects_incharge,'projects_completed':projects_completed})
    else:
        form = DateRangeInput()
    return render(request,'_layout.html',{'form':form,'data':uri,'value':80,'subtasks':subtasks,
    'projects_incharge':projects_incharge,'projects_completed':projects_completed})





def deadline_score(request):
    labels=[]
    data =[]

    queryset_one=SubTask.objects.filter(member_assigned=request.user)
    # queryset_two=SubTask.objects.filter(Q(task_due_date__gte=start_date) & Q(task_due_date__lte=end_date) & Q(member_assigned=request.user))
    
    months_of_the_year=[]

    for i in range(1,12):
        months_of_the_year.append(calendar.month_name[i])

    for subtask in queryset_one:
        labels.append(subtask.task_due_date.strftime("%d %b"))
        data.append(subtask.subtask_deadline_score)


    return JsonResponse(data={
        'labels':labels,
        'data':data
    })


def resubmission_score(request):
    labels=[]
    data =[]

    queryset_one=SubTask.objects.filter(member_assigned=request.user)
    # queryset_two=SubTask.objects.filter(Q(task_due_date__gte=start_date) & Q(task_due_date__lte=end_date) & Q(member_assigned=request.user))
    
    months_of_the_year=[]

    for i in range(1,12):
        months_of_the_year.append(calendar.month_name[i])

    for subtask in queryset_one:
        labels.append(subtask.task_due_date.strftime("%d %b"))
        data.append(subtask.subtask_resubmission_score)


    return JsonResponse(data={
        'labels':labels,
        'data':data
    })


def reset_score(request):
    labels=[]
    data =[]

    queryset_one=SubTask.objects.filter(member_assigned=request.user)
    # queryset_two=SubTask.objects.filter(Q(task_due_date__gte=start_date) & Q(task_due_date__lte=end_date) & Q(member_assigned=request.user))
    
    months_of_the_year=[]

    for i in range(1,12):
        months_of_the_year.append(calendar.month_name[i])

    for subtask in queryset_one:
        labels.append(subtask.task_due_date.strftime("%d %b"))
        data.append(subtask.subtask_deadline_reset_score)


    return JsonResponse(data={
        'labels':labels,
        'data':data
    })


def quality_score(request):
    labels=[]
    data =[]

    queryset_one=SubTask.objects.filter(member_assigned=request.user)
    # queryset_two=SubTask.objects.filter(Q(task_due_date__gte=start_date) & Q(task_due_date__lte=end_date) & Q(member_assigned=request.user))
    
    months_of_the_year=[]

    for i in range(1,12):
        months_of_the_year.append(calendar.month_name[i])

    for subtask in queryset_one:
        labels.append(subtask.task_due_date.strftime("%d %b"))
        data.append(subtask.rating)


    return JsonResponse(data={
        'labels':labels,
        'data':data
    })
    


def planning_score(request):
    labels=[]
    data =[]

    queryset_one=SubTask.objects.filter(member_assigned=request.user)
    # queryset_two=SubTask.objects.filter(Q(task_due_date__gte=start_date) & Q(task_due_date__lte=end_date) & Q(member_assigned=request.user))
    
    months_of_the_year=[]

    for i in range(1,12):
        months_of_the_year.append(calendar.month_name[i])

    for subtask in queryset_one:
        labels.append(subtask.task_due_date.strftime("%d %b"))
        data.append(subtask.subtask_planning_score)


    return JsonResponse(data={
        'labels':labels,
        'data':data
    })
    


