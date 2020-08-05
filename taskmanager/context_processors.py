from taskmanager.models.tasks import Task,Team,TaskAnalysis,SubTaskAnalysis,SubTask
from django.db.models import Q,Avg,Count

def get_teams(request):
    teamset=Team.objects.all()
    return dict(teamset=teamset)


def get_task_analysis(request):
    task_data=Task.objects.all()
    task_resubmits=TaskAnalysis.objects.filter(Q(resubmits='RES')).annotate(num_tasks_resubmitted=Count('task'))
    task_resets=TaskAnalysis.objects.filter(~Q(resubmits='RES')).annotate(num_tasks_reset=Count('task'))
    return dict(task_resubmits=task_resubmits,task_resets=task_resets,task_data=task_data)


def get_subtask_analysis(request):
    subtask_data=SubTask.objects.all()
    subtask_resubmits=SubTaskAnalysis.objects.filter(Q(resubmits='RES')).annotate(num_subtasks_resubmitted=Count('subtask',distinct=True))
    subtask_resets=SubTaskAnalysis.objects.filter(~Q(resubmits='RES')).annotate(num_subtasks_reset=Count('subtask',distinct=True))
    return dict(subtask_resets=subtask_resets,subtask_resubmits=subtask_resubmits,subtask_data=subtask_data)


