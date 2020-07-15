from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from taskmanager.models.tasks import Team
from taskmanager.forms.taskforms import DateRangeInput
from taskmanager.models.tasks import Task,Team,TaskAnalysis,SubTaskAnalysis,SubTask
from django.db.models import Avg,Q,Sum,Max
from datetime import datetime


def split_dates(data):
    splitted_data=data.split()
    splitted_data.remove('-')
    return splitted_data

def to_datetime(data):
    converted_date = datetime.strptime(data, "%m/%d/%Y")
    return converted_date

# @require_http_methods(["GET"])
def index(request):
    if request.method == 'POST':
        form = DateRangeInput(request.POST or None)
        if form.is_valid():
            date_range=form.cleaned_data.get('date_range_picker')
            splitted_dates = split_dates(date_range)
            start_date= to_datetime(splitted_dates[0])
            end_date=to_datetime(splitted_dates[1])
            project_sets = TaskAnalysis.objects.filter(Q(revised_due_date__gte=start_date) & Q(revised_due_date__lte=end_date))
            # import pdb; pdb.set_trace()
            return render(request,'_layout.html',{'form':form,'project_sets':project_sets,'date_range':date_range})
    else:
        form = DateRangeInput()
    return render(request,'_layout.html',{'form':form,})



