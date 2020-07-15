from django.contrib import admin
from .models import Task, Team, Comment,TaskReview,SubTask,TaskAnalysis,SubTaskAnalysis

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Team)
admin.site.register(Comment)
admin.site.register(TaskReview)
admin.site.register(TaskAnalysis)
admin.site.register(SubTaskAnalysis)
