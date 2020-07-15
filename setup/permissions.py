from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType
from taskmanager.models.tasks import Task,Team,SubTask


# initialize the contenttypes over here
task_content_type=ContentType.objects.get_for_model(Task)
subtask_content_type=ContentType.objects.get_for_model(SubTask)
team_content_type=ContentType.objects.get_for_model(Team)

# create the permissions over here
permission_format=Permission.objects.create(
    codename='can_see_results',
    name='Can see results',
    content_type=task_content_type
)

##################
# task permissions

revise_due_date=Permission.objects.create(
    codename='can_revise_due_dates',
    name='can revise due dates',
    content_type=task_content_type
)

reassign_task=Permission.objects.create(
    codename='can_reassign_task',
    name='can reassign task',
    content_type=task_content_type
)

rate_task=Permission.objects.create(
    codename='can_rate_task',
    name='can rate task',
    content_type=task_content_type
)


return_task=Permission.objects.create(
    codename='can_return_task',
    name='can return task',
    content_type=task_content_type
)


approve_task_completion=Permission.objects.create(
    codename='can_approve_task_completion',
    name='can approve task completion',
    content_type=task_content_type
)

approve_returned_task=Permission.objects.create(
    codename='can_approve_returned_task',
    name='can approve returned task',
    content_type=task_content_type
)

approve_revise_due_date=Permission.objects.create(
    codename='can_approve_revise_due_date',
    name='can approve revise due date',
    content_type=task_content_type
)

approve_task_change=Permission.objects.create(
    codename='can_approve_task_change',
    name='can approve task change',
    content_type=task_content_type
)

approve_task_delete=Permission.objects.create(
    codename='can_approve_task_delete',
    name='can approve task delete',
    content_type=task_content_type
)


##################
# subtask permissions

revise_due_date=Permission.objects.create(
    codename='can_revise_due_dates',
    name='can revise due dates',
    content_type=task_content_type
)

reassign_task=Permission.objects.create(
    codename='can_reassign_task',
    name='can reassign task',
    content_type=subtask_content_type
)

rate_task=Permission.objects.create(
    codename='can_rate_task',
    name='can rate task',
    content_type=subtask_content_type
)


return_task=Permission.objects.create(
    codename='can_return_task',
    name='can return task',
    content_type=subtask_content_type
)


approve_task_completion=Permission.objects.create(
    codename='can_approve_task_completion',
    name='can approve task completion',
    content_type=subtask_content_type
)

approve_returned_task=Permission.objects.create(
    codename='can_approve_returned_task',
    name='can approve returned task',
    content_type=subtask_content_type
)

approve_revise_due_date=Permission.objects.create(
    codename='can_approve_revise_due_date',
    name='can approve revise due date',
    content_type=task_content_type
)

approve_task_change=Permission.objects.create(
    codename='can_approve_task_change',
    name='can approve task change',
    content_type=subtask_content_type
)

approve_task_delete=Permission.objects.create(
    codename='can_approve_task_delete',
    name='can approve task delete',
    content_type=subtask_content_type
)

####################
# team permissions #
####################

add_team_member=Permission.objects.create(
    codename='can_add_team_member',
    name='can add team member',
    content_type=team_content_type
)

remove_team_member=Permission.objects.create(
    codename='can_remove_team_member',
    name='can remove team member',
    content_type=team_content_type
)

transfer_team_member=Permission.objects.create(
    codename='can_transfer_team_member',
    name='can transfer team member',
    content_type=team_content_type
)

request_team_delete=Permission.objects.create(
    codename='can_request_team_delete',
    name='can request team delete',
    content_type=team_content_type
)

assign_team_leader=Permission.objects.create(
    codename='can_assign_team_leader',
    name='can assign team leader',
    content_type=team_content_type
)

transfer_team_leader=Permission.objects.create(
    codename='can_transfer_team_leader',
    name='can transfer team leader',
    content_type=team_content_type
)

approve_team_create=Permission.objects.create(
    codename='can_approve_team_create',
    name='can approve team create',
    content_type=team_content_type
)

approve_team_delete=Permission.objects.create(
    codename='can_approve_team_delete',
    name='can approve team delete',
    content_type=team_content_type
)

approve_team_member_add=Permission.objects.create(
    codename='can_approve_team_member_add',
    name='can approve team member add',
    content_type=team_content_type
)

approve_team_member_remove=Permission.objects.create(
    codename='can_approve_team_member_remove',
    name='can approve team member transfer',
    content_type=team_content_type
)

approve_team_member_transfer=Permission.objects.create(
    codename='can_approve_team_member_transfer',
    name='can approve team member transfer',
    content_type=team_content_type
)

approve_team_leader_add=Permission.objects.create(
    codename='can_approve_team_leader_add',
    name='can appprove team leader add',
    content_type=team_content_type
)

approve_team_leader_transer=Permission.objects.create(
    codename='can_approve_team_leader_transfer',
    name='can approve team leader transfer',
    content_type=team_content_type
)

approve_team_leader_remove=Permission.objects.create(
    codename='can_appprove_team_leader_transfer',
    name='can approve team leader transfer',
    content_type=team_content_type
)


###############################################
# group permissions into their specific lists #
###############################################
team_member_permissions=[
    revise_due_date,reassign_task
]
team_leader_permissions=[
    reassign_task,rate_task,return_task,
    approve_task_completion,approve_returned_task,
    approve_task_change,add_team_member,approve_revise_due_date,
    remove_team_member,transfer_team_member,
]
business_head_permissions=[
    request_team_delete,assign_team_leader,
    transfer_team_leader,approve_team_member_add,
    approve_team_member_transfer,approve_team_member_remove,
    approve_task_delete
]

organization_leader_permission=[
    approve_team_create,approve_team_delete,
    approve_team_leader_transer,approve_team_leader_remove,
    approve_team_leader_add
]

#############################
# register groups over here #
#############################
organizational_leader_group,created=Group.objects.create(name='organization_leaders')
business_head_group,created=Group.objects.create(name='business_heads')
team_leader_group,created=Group.objects.create(name='team_leaders')
team_member_group,created=Group.objects.create(name='team_members')

###########################################
# assign set of permissions to that group #
###########################################
team_member_group.permissions.add(team_member_permissions)
team_leader_group.permissions.add(team_leader_permissions)
business_head_group.permissions.add(business_head_permissions)
organizational_leader_group.permissions.add(organization_leader_permission)

