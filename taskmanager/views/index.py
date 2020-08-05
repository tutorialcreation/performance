# pylint: disable=E1101

from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,JsonResponse
from taskmanager.models.tasks import Team
from taskmanager.forms.taskforms import DateRangeInput
from taskmanager.models.tasks import Task,Team,TaskAnalysis,SubTaskAnalysis,SubTask,DateRanges
from django.contrib.auth.models import User
from django.db.models import Avg,Q,Sum,Max,Count
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from django.core import serializers
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.style as mplstyle
import mplcursors
import requests
import pandas as pd
import numpy as np
import math
import itertools
import statistics
import io
import calendar
import urllib,base64

def split_dates(data):
    #data
    splitted_data=data.split()
    splitted_data.remove('-')
    return splitted_data

def to_datetime(data):
    converted_date = datetime.strptime(data, "%m/%d/%Y").date()
    return converted_date



def index(request):
    subtasks=SubTask.objects.filter(member_assigned=request.user)
    all_teams=set()
    for index in range(len(subtasks)):
        all_teams.add(subtasks[index].task.team)
    all_teams=list(all_teams)
    teams=Team.objects.filter(name__in=all_teams)
    all_members=set()
    for index in range(len(teams)):
        all_members.add(teams[index].members.all())
    all_members=list(set(itertools.chain.from_iterable(all_members)))

    projects_incharge=Task.objects.filter(assigned_to=request.user)
    projects_completed=Task.objects.filter(Q(assigned_to=request.user) & Q(subtask__status='COMP'))
    if request.user.is_authenticated and request.method=='POST':
        form=DateRangeInput(request.POST or None)
        member=request.POST.get('team_member')
        team=request.POST.get('teamset')
        # print(member)
        if form.is_valid():
            date_range=form.cleaned_data.get('date_range_picker')
            date_frequency=form.cleaned_data.get('date_frequencies')
            DateRanges.objects.create(date_range=date_range,date_frequency=date_frequency,member=member,team=team)
            splitted_dates=split_dates(date_range)
            start_date=to_datetime(splitted_dates[0])
            end_date=to_datetime(splitted_dates[1])
            project_set=Task.objects.filter(Q(completed_date__gte=start_date) & Q(completed_date__lte=end_date))
            subtask_set=SubTask.objects.filter(Q(completed_date__gte=start_date) & Q(completed_date__lte=end_date))
            if form.cleaned_data.get('date_range_picker') and not form.cleaned_data.get('multiple_date_picker'):
                subtasks=SubTask.objects.filter(Q(task_due_date__gte=start_date) & Q(task_due_date__lte=end_date) & Q(member_assigned=request.user))
            else:
                multiple_dates=form.cleaned_data.get('multiple_date_picker').split(',')
                multiple_value_dates=[datetime.strptime(data,"%m/%d/%Y") for data in multiple_dates]
                subtasks=SubTask.objects.filter(Q(task_due_date__in=multiple_value_dates) & Q(member_assigned=request.user))
            subtasks=SubTask.objects.filter(member_assigned=request.user)
            return render(request,'_layout.html',{
                'form':form,
                'subtasks':subtasks,
                'projects_incharge':projects_incharge,
                'projects_completed':projects_completed
            })
    else:
        form=DateRangeInput()
        return render(request,'_layout.html',{
            'form':form,
            'subtasks':subtasks, 
            'all_members':all_members,
            'projects_incharge':projects_incharge,
            'projects_completed':projects_completed
        })


def postDateRange(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = DateRangeInput(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)




def deadline_score(request):
    dates=DateRanges.objects.all().last()
    if dates.date_range and dates.date_frequency:
        date_range=dates.date_range
        date_frequency=dates.date_frequency
        date_member=dates.member
        team=dates.team

        splitted_dates=split_dates(date_range)
        start_date=to_datetime(splitted_dates[0])
        end_date=to_datetime(splitted_dates[1])
        date_ranges=pd.date_range(start_date,end_date,freq=date_frequency)
        # import pdb;pdb.set_trace()
        date_ranges=date_ranges.to_pydatetime().tolist()
        if request.user.is_superuser:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task__team__name=team) & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        elif request.user.is_staff:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        else:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)& Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')

        df = pd.DataFrame({
            'Due Date': [subtask.task_due_date for subtask in subtasks],
            'Deadline Score': [subtask.subtask_deadline_score for subtask in subtasks]
        })
        
        df=df.groupby(['Due Date'],as_index=False).mean()

        df=df.dropna()
        results=df.to_dict('records')

        return JsonResponse(data={
            'labels':[results[date_]['Due Date'].strftime("%d %b") for date_ in range(len(results))],
            'data':[results[deadline_]['Deadline Score'] for deadline_ in range(len(results))]

        })
    else:
        return JsonResponse(data={
            'labels':['30 Jul','30 Aug','12 Dec'],
            'data':[0.23,0.45,0.67]
        })

    
def resubmission_score(request):
    dates=DateRanges.objects.all().last()
    if dates.date_range and dates.date_frequency:
        date_range=dates.date_range
        date_frequency=dates.date_frequency
        date_member=dates.member
        team=dates.team

        splitted_dates=split_dates(date_range)
        start_date=to_datetime(splitted_dates[0])
        end_date=to_datetime(splitted_dates[1])
        date_ranges=pd.date_range(start_date,end_date,freq=date_frequency)
        date_ranges=date_ranges.to_pydatetime().tolist()
        if request.user.is_superuser:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task__team__name=team) & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        elif request.user.is_staff:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        else:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)& Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')

        
        df = pd.DataFrame({
            'Due Date': [subtask.task_due_date for subtask in subtasks],
            'Deadline Score': [subtask.subtask_resubmission_score for subtask in subtasks]
        })
        
        df=df.groupby(['Due Date'],as_index=False).mean()

        df=df.dropna()
        results=df.to_dict('records')

        return JsonResponse(data={
            'labels':[results[date_]['Due Date'].strftime("%d %b") for date_ in range(len(results))],
            'data':[results[deadline_]['Deadline Score'] for deadline_ in range(len(results))]

        })
    else:
        return JsonResponse(data={
            'labels':['30 Jul','30 Aug','12 Dec'],
            'data':[0.23,0.45,0.67]
        })
    



def reset_score(request):
    dates=DateRanges.objects.all().last()
    if dates.date_range and dates.date_frequency:
        date_range=dates.date_range
        date_frequency=dates.date_frequency
        date_member=dates.member
        team=dates.team
        
        splitted_dates=split_dates(date_range)
        start_date=to_datetime(splitted_dates[0])
        end_date=to_datetime(splitted_dates[1])
        date_ranges=pd.date_range(start_date,end_date,freq=date_frequency)
        date_ranges=date_ranges.to_pydatetime().tolist()
        if request.user.is_superuser:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task__team__name=team) & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        elif request.user.is_staff:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        else:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)& Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')

        df = pd.DataFrame({
            'Due Date': [subtask.task_due_date for subtask in subtasks],
            'Deadline Score': [subtask.subtask_deadline_reset_score for subtask in subtasks]
        })
        
        df=df.groupby(['Due Date'],as_index=False).mean()

        df=df.dropna()
        results=df.to_dict('records')

        return JsonResponse(data={
            'labels':[results[date_]['Due Date'].strftime("%d %b") for date_ in range(len(results))],
            'data':[results[deadline_]['Deadline Score'] for deadline_ in range(len(results))]

        })
    else:
        return JsonResponse(data={
            'labels':['30 Jul','30 Aug','12 Dec'],
            'data':[0.23,0.45,0.67]
        })

def quality_score(request):
    dates=DateRanges.objects.all().last()
    if dates.date_range and dates.date_frequency:
        date_range=dates.date_range
        date_frequency=dates.date_frequency
        date_member=dates.member
        team=dates.team

        splitted_dates=split_dates(date_range)
        start_date=to_datetime(splitted_dates[0])
        end_date=to_datetime(splitted_dates[1])
        date_ranges=pd.date_range(start_date,end_date,freq=date_frequency)
        date_ranges=date_ranges.to_pydatetime().tolist()
        if request.user.is_superuser:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task__team__name=team) & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        elif request.user.is_staff:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        else:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)& Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')

        df = pd.DataFrame({
            'Due Date': [subtask.task_due_date for subtask in subtasks],
            'Deadline Score': [subtask.rating for subtask in subtasks]
        })
        
        df=df.groupby(['Due Date'],as_index=False).mean()

        df=df.dropna()
        results=df.to_dict('records')

        return JsonResponse(data={
            'labels':[results[date_]['Due Date'].strftime("%d %b") for date_ in range(len(results))],
            'data':[results[deadline_]['Deadline Score'] for deadline_ in range(len(results))]

        })
    else:
        return JsonResponse(data={
            'labels':['30 Jul','30 Aug','12 Dec'],
            'data':[0.23,0.45,0.67]
        })

def planning_score(request):
    dates=DateRanges.objects.all().last()
    if dates.date_range and dates.date_frequency:
        date_range=dates.date_range
        date_frequency=dates.date_frequency
        date_member=dates.member
        team=dates.team
        
        splitted_dates=split_dates(date_range)
        start_date=to_datetime(splitted_dates[0])
        end_date=to_datetime(splitted_dates[1])
        date_ranges=pd.date_range(start_date,end_date,freq=date_frequency)
        date_ranges=date_ranges.to_pydatetime().tolist()
        if request.user.is_superuser:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task__team__name=team) & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        elif request.user.is_staff:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)|Q(member_assigned__username=date_member) 
            & Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')
        else:
            subtasks=SubTask.objects.filter(
            Q(member_assigned=request.user)& Q(task_due_date__in=date_ranges)
            ).order_by('task_due_date')

        df = pd.DataFrame({
            'Due Date': [subtask.task_due_date for subtask in subtasks],
            'Deadline Score': [subtask.subtask_planning_score for subtask in subtasks]
        })
        
        df=df.groupby(['Due Date'],as_index=False).mean()

        df=df.dropna()
        results=df.to_dict('records')

        return JsonResponse(data={
            'labels':[results[date_]['Due Date'].strftime("%d %b") for date_ in range(len(results))],
            'data':[results[deadline_]['Deadline Score'] for deadline_ in range(len(results))]

        })
    else:
        return JsonResponse(data={
            'labels':['30 Jul','30 Aug','12 Dec'],
            'data':[0.23,0.45,0.67]
        })
    


