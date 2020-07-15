from taskmanager.models.tasks import Task,Team,TaskAnalysis,SubTaskAnalysis,SubTask
from django.db.models import Q,Avg

def get_teams(request):
    teamset=Team.objects.all()
    return dict(teamset=teamset)


def get_task_analysis(request):
    task_data=Task.objects.all()
    task_resubmits=TaskAnalysis.objects.filter(Q(resubmits='RES'))
    task_resets=TaskAnalysis.objects.filter(~Q(resubmits='RES'))
    return dict(task_resubmits=task_resubmits,task_resets=task_resets,task_data=task_data)


def get_subtask_analysis(request):
    subtask_data=SubTask.objects.all()
    subtask_resubmits=SubTaskAnalysis.objects.filter(Q(resubmits='RES'))
    subtask_resets=SubTaskAnalysis.objects.filter(~Q(resubmits='RES'))
    return dict(subtask_resets=subtask_resets,subtask_resubmits=subtask_resubmits,subtask_data=subtask_data)


