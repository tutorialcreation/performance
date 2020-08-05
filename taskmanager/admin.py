from django.contrib import admin
from .models import (
    Task, Team, Comment,
    TaskReview,SubTask,TaskAnalysis,
    SubTaskAnalysis,
    DateRanges,NotificationSet,
    TaskSource,BidOrAwardAnalyzer,
    BiddedTask,InvoiceDetail
)

class TaskAdmin(admin.ModelAdmin):
    list_display=('id','title',)


admin.site.register(Task,TaskAdmin)
admin.site.register(SubTask)
admin.site.register(Team)
admin.site.register(Comment)
admin.site.register(TaskReview)
admin.site.register(TaskAnalysis)
admin.site.register(SubTaskAnalysis)
admin.site.register(DateRanges)
admin.site.register(NotificationSet)
admin.site.register(TaskSource)
admin.site.register(BidOrAwardAnalyzer)
admin.site.register(BiddedTask)
admin.site.register(InvoiceDetail)