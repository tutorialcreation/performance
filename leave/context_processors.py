from .models import Leave
from django.db.models import Q,Avg,Count

def get_leaves(request):
    leaveset=Leave.objects.all()
    return dict(leaveset=leaveset)
