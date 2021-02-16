"""Task Manager URL Configuration

"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from taskmanager import views

# from . import views

app_name = 'taskmanager'

urlpatterns = [
    path('', views.index, name='index'),
    path('dates/',views.postDateRange,name='date_ranges'),
    path('ajax/charts/deadline/', views.deadline_score, name='chart_deadline'),
    path('ajax/charts/resubmission/', views.resubmission_score, name='chart_resubmission'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('ajax/charts/reset/', views.reset_score, name='chart_reset'),
    path('ajax/charts/quality/', views.quality_score, name='chart_quality'),
    path('charts/planning/', views.planning_score, name='chart_planning'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('team_details/<int:team_id>/', views.team_details, name='team_details'),
    path('teams/create/', views.team_create, name='team_create'),
    path('teams/<int:team_id>/remove-member/', views.team_remove_member, name='team_remove_member'),
    path('teams/<int:team_id>/add-member/', views.team_add_member, name='team_add_member'),
    path('teams/<int:team_id>/delete/', views.team_delete, name='team_delete'),
    path('my-tasks/', views.tasks, name='task_my_tasks'),
    path('team-tasks/<int:team_id>/', views.team_tasks, name='team_tasks'),
    path('tasks/<int:pk>/update/', views.TaskUpdate.as_view(), name='task_update'),
    path('tasks/<int:pk>/reassign/', views.Reassigning.as_view(), name='task_reassign'),
    path('tasks/invoice_assignment/', views.RequestInvoice.as_view(), name='invoice_assignment'),
    path('tasks/<int:pk>/extend/', views.ExtendDeadline.as_view(), name='task_extend'),
    path('tasks/bid_create/', views.TaskBidCreate.as_view(), name='task_bid_create'),
    path('tasks/report_create/', views.ReportCreate.as_view(), name='report_create'),
    path('tasks/<int:pk>/bid/', views.TaskBid.as_view(), name='task_bid'),
    path('tasks/<int:pk>/rating/', views.Rating.as_view(), name='task_rating'),
    path('sub_tasks/<int:pk>/rating/', views.SubTaskRating.as_view(), name='subtask_rating'),
    path('sub_tasks/<int:pk>/return/', views.Revision.as_view(), name='subtask_return'),
    path('tasks/<int:task_id>/comment/', views.task_comment, name='task_comment'),
    path('tasks/<int:task_id>/accept/', views.task_accept, name='task_accept'),
    path('tasks/<int:task_id>/resubmit/', views.task_resubmit, name='task_resubmit'),
    path('tasks/<int:task_id>/mark-completed/', views.task_mark_completed, name='task_mark_completed'),
    path('tasks/<int:task_id>/mark-pending-approved/', views.task_mark_pending_approved, name='task_mark_pending_approved'),
    path('tasks/<int:task_id>/return-revision/', views.task_mark_revision, name='task_mark_revision'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/create/', views.TaskCreate.as_view(), name='task_create'),
    path('tasks/search/', views.task_search, name='task_search'),
    path('tasks/sources/',views.task_sources,name='task_source'),
    path('signup/', views.signup, name='signup'),
    path('ajax/load-members/', views.load_members, name='ajax_load_members'),
    path('ajax/load-projects/', views.load_projects, name='ajax_load_projects'),

]

