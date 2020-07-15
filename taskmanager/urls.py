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
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('team_details/<int:team_id>/', views.team_details, name='team_details'),
    path('teams/create/', views.team_create, name='team_create'),
    path('teams/<int:team_id>/remove-member/', views.team_remove_member, name='team_remove_member'),
    path('teams/<int:team_id>/add-member/', views.team_add_member, name='team_add_member'),
    path('teams/<int:team_id>/delete/', views.team_delete, name='team_delete'),
    path('my-tasks/', views.tasks, name='task_my_tasks'),
    path('team-tasks/<int:team_id>/', views.team_tasks, name='team_tasks'),
    path('my-completed-tasks/', views.completed_tasks, name='task_completed_tasks'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/update/', views.TaskUpdate.as_view(), name='task_update'),
    path('tasks/<int:pk>/reassign/', views.Reassigning.as_view(), name='task_reassign'),
    path('tasks/<int:pk>/rating/', views.Rating.as_view(), name='task_rating'),
    path('sub_tasks/<int:pk>/rating/', views.SubTaskRating.as_view(), name='subtask_rating'),
    path('tasks/<int:task_id>/comment/', views.task_comment, name='task_comment'),
    path('tasks/<int:task_id>/accept/', views.task_accept, name='task_accept'),
    path('tasks/<int:task_id>/resubmit/', views.task_resubmit, name='task_resubmit'),
    path('tasks/<int:task_id>/mark-completed/', views.task_mark_completed, name='task_mark_completed'),
    path('tasks/<int:task_id>/mark-approved/', views.task_mark_approved, name='task_mark_approved'),
    path('tasks/<int:task_id>/return-revision/', views.task_mark_revision, name='task_mark_revision'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/create/', views.TaskCreate.as_view(), name='task_create'),
    path('tasks/search/', views.task_search, name='task_search'),
    # path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    # path('logout/', views.logout, name='logout'),
    path('ajax/load-members/', views.load_members, name='ajax_load_members'),
    path('ajax/load-projects/', views.load_projects, name='ajax_load_projects'),
]

# urlpatterns += [
# ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
