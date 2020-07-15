from django.shortcuts import render
from taskmanager.models import Task,Team


def index_view(request):
	team=Team.objects.all()
	return render(request,'index.html',{'teams':team})


def bootstrap_index(request):
	return render(request,'bootstrap_site_template/base.html')