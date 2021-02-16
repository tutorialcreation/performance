from crm.models import FilterSet
from django.db.models import Q,Avg,Count

def existing_filters(request):
    if request.user.is_authenticated:
        existing_filters=FilterSet.objects.filter(user_filters=request.user).values("search_parameter").annotate(n=Count("pk"))
        # import pdb;pdb.set_trace()
        return dict(existing_filters=existing_filters)
    else:
        existing_filters=FilterSet.objects.all().values("search_parameter").annotate(n=Count("pk"))
        return dict(existing_filters=existing_filters)