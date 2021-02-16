from taskmanager.views.auth import login, signup, logout
from taskmanager.views.teams import (
    team_create, team_detail, team_add_member, team_remove_member, team_delete,team_details
)
from taskmanager.views.index import (
    index,deadline_score,resubmission_score,
    reset_score,quality_score,planning_score,
    postDateRange
)
from taskmanager.views.tasks import (
    tasks,task_accept, task_mark_completed, task_comment, task_delete,task_detail,
    task_mark_revision,TaskCreate,load_members,TaskUpdate,Rating,
    Reassigning,task_resubmit,team_tasks,load_projects,SubTaskRating,task_mark_pending_approved,
    ExtendDeadline,Revision,task_sources,TaskBid,TaskBidCreate,RequestInvoice,ReportCreate
)
from taskmanager.views.search import task_search
