import datetime
from datetime import datetime
import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save,pre_save,post_init,pre_init
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.db.models.signals import post_save,post_init
from django.dispatch import receiver
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from setup.utils import convert_to_seconds


# Get user model defined in settings.AUTH_USER_MODEL
# Better to call get_user_model in pluggable app instead of imporing User from django.contrib.auth.models
UserModel = get_user_model()




class Team(models.Model):
    """
    Not using Django's built-in Group model because we want
    to save the creater of team.
    """
    name = models.CharField(max_length=50)
    desc = models.TextField(default='', max_length=1024, blank=True)
    leader = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='leading_teams')
    members = models.ManyToManyField(UserModel)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("taskmanager:team_detail", kwargs={"team_id": self.id})

    def get_absolute_urls(self):
        return reverse("taskmanager:team_details", kwargs={"team_id": self.id})


    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Teams"


class Task(models.Model):
    ASSIGNMENT_TYPE=[
        ('one','Type One'),
        ('two','Type Two'),
        ('other','OTHER')
    ]
    RATING_RANGE=[
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5')
    ]
    STATUS_CHOICES = (
        ('PLAN', 'Begin'),
        ('PROG', 'On going'),
        ('COMP', 'Completed'),
        ('RES',  'Resubmit'),
        ('PA',   'Pending Approval'),
        ('APP',  'Approved'),
        ('REV',  'Revise'),
        ('RET',  'Resubmitted'),
    )
    DEFAULT_ASSIGMENT_TYPE=1
    title = models.CharField('Project Name',max_length=50,null=True)
    assignment_type=models.CharField('*',max_length=50,null=True,blank=True,)
    assignment_typeset=models.ForeignKey('self',on_delete=models.CASCADE,null=True,verbose_name='Project Type',blank=True)
    desc = models.TextField(default="test", max_length=1024, null=True,blank=True)
    sub_tasks=JSONField(null=True,blank=True)
    client_code = models.TextField(default="test", max_length=1024, null=True,blank=True)
    client_name = models.CharField('Client',max_length=50,null=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PLAN',null=True)

    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='created_tasks',null=True)

    # A task can be assigned to one or many users
    assigned_to = models.ManyToManyField(UserModel, help_text="Press ctrl to select multiple",verbose_name='Project Coordinator')

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    planned_date = models.DateField(auto_now_add=True)
    accepted_date = models.DateField(null=True, blank=True)
    accepted_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='accepted_tasks',
                                    blank=True)
    due_date = models.DateTimeField('Project Due Date',null=True)
    revised_due_date = models.DateTimeField(null=True, blank=True)
    date_accepted = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    rating=models.IntegerField(choices=RATING_RANGE,null=True)
    content=models.CharField('comments',max_length=500)
    team_leader=models.BooleanField(default=False)
    approved_date=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.assignment_type if self.assignment_type else ''

    def get_absolute_url(self):
        return reverse("taskmanager:task_detail", kwargs={"task_id": self.id})

    @property
    def deadline_score(self):
        approved_delta=relativedelta(self.date_accepted,self.approved_date)
        deadline_delta=relativedelta(self.date_accepted,self.due_date)
        if deadline_delta and approved_delta:
            deadline_score=convert_to_seconds(approved_delta)/convert_to_seconds(deadline_delta)
            return round(deadline_score,3)

    @property
    def task_resubmission_score(self):
        resubmitted_tasks=TaskAnalysis.objects.filter(Q(resubmits='RES') & Q(task__creator=self.creator)).count()
        total_tasks=Task.objects.filter(creator=self.creator).count()
        resubmission_score=(1-(resubmitted_tasks/total_tasks))
        return round(resubmission_score,3)


    @property
    def task_deadline_reset_score(self):
        reset_tasks=TaskAnalysis.objects.filter(~Q(resubmits='RES') & Q(task__creator=self.creator)).count()
        total_tasks=Task.objects.filter(creator=self.creator).count()
        deadline_reset_score=(1-(reset_tasks/total_tasks))
        return round(deadline_reset_score,3)


    @property
    def task_count(self):
        completed_tasks=self.subtask.filter(status='COMP').count()
        total_tasks=self.subtask.all().count()
        if completed_tasks == 0 or total_tasks == 0:
            rate=0
        else:
            rate = completed_tasks/total_tasks
        return round(rate * 100)


    # Has due date for an instance of this object passed?
    def is_overdated(self):
        """Returns whether the Tasks's due date has passed or not."""
        if self.due_date and  timezone.now() > self.due_date:
            return True
        else:
            return False


        
    
    class Meta:
        ordering = ["planned_date"]
        verbose_name_plural = "Tasks"





class SubTask(models.Model):
    STATUS_CHOICES = (
        ('PLAN', 'To Accept'),
        ('PROG', 'On going'),
        ('COMP', 'Completed'),
        ('RES',  'Resubmit'),
        ('PA',   'Pending Approval'),
        ('APP',  'Approved'),
        ('REV',  'Revise'),
        ('RET',  'Resubmitted'),
    )
    RATING_RANGE=[
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5')
    ]
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PLAN',null=True)
    name=models.CharField(max_length=300)
    task=models.ForeignKey(Task,related_name='subtask',on_delete=models.CASCADE)
    member_assigned=models.ForeignKey(UserModel,related_name='assignee_subtask', on_delete=models.CASCADE,verbose_name='Assign Task to:')
    team=models.ForeignKey(Team,on_delete=models.CASCADE,null=True,blank=True)
    task_due_date=models.DateTimeField('Task Due Date:',null=True)
    prior_task=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    date_accepted = models.DateTimeField(null=True, blank=True)
    approved_date=models.DateTimeField(null=True,blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    revised_due_date=models.DateTimeField(null=True,blank=True)
    rating=models.IntegerField(choices=RATING_RANGE,null=True)
    content=models.CharField('comments',max_length=500,null=True)

    def __str__(self):
        return self.name



    @property
    def subtask_deadline_score(self):
        deadline_delta=relativedelta(self.date_accepted,self.task_due_date)
        approved_delta=relativedelta(self.date_accepted,self.approved_date)
        if deadline_delta and approved_delta:
            deadline_score=convert_to_seconds(deadline_delta)/convert_to_seconds(approved_delta)
            return round((1/deadline_score),3)

    @property
    def subtask_planning_score(self):
        approved_delta=relativedelta(self.task_due_date,self.approved_date)
        deadline_delta=relativedelta(self.task_due_date,self.date_accepted)
        if deadline_delta and approved_delta:
            planning_score=convert_to_seconds(approved_delta)/convert_to_seconds(deadline_delta)
            return round((1-planning_score),3)



    @property
    def subtask_rate(self):
        completed_tasks=SubTask.objects.filter(Q(status='COMP') & Q(member_assigned=self.member_assigned)).count()
        total_tasks=SubTask.objects.filter(Q(member_assigned=self.member_assigned)).count()
        # import pdb; pdb.set_trace()
        if completed_tasks == 0 or total_tasks == 0:
            rate=0
        else:
            rate = completed_tasks/total_tasks
        return round(rate * 100)

    @property
    def subtask_resubmission_score(self):
        resubmitted_tasks=SubTaskAnalysis.objects.filter(Q(resubmits='RES') & Q(subtask__member_assigned=self.member_assigned)).count()
        total_tasks=SubTask.objects.filter(member_assigned=self.member_assigned).count()
        resubmission_score=(1-(resubmitted_tasks/total_tasks))
        return round(resubmission_score,3)


    @property
    def subtask_deadline_reset_score(self):
        reset_tasks=SubTaskAnalysis.objects.filter(~Q(resubmits='RES') & Q(subtask__member_assigned=self.member_assigned)).count()
        total_tasks=SubTask.objects.filter(member_assigned=self.member_assigned).count()
        deadline_reset_score=(1-(reset_tasks/total_tasks))
        return round(deadline_reset_score,3)

    

    @property
    def pending_tasks(self):
        completed_tasks=SubTask.objects.filter(Q(status='COMP') & Q(member_assigned=self.member_assigned)).count()
        total_tasks=SubTask.objects.filter(Q(member_assigned=self.member_assigned)).count()
        # import pdb; pdb.set_trace()
        if completed_tasks == 0 or total_tasks == 0:
            pending=0
        else:
            pending = total_tasks - completed_tasks
        return pending


    def is_overdated(self):
        """Returns whether the Tasks's due date has passed or not."""
        if self.task_due_date and  timezone.now() > self.task_due_date:
            return True
        else:
            return False



class Comment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment_datetime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def snippet(self):
        """
        Returns a short version of comment body with auther's username as prefix
        """
        return "{author} - {snippet}...".format(author=self.author, snippet=self.body[:36])

    def __str__(self):
        return self.snippet()

    class Meta:
        ordering = ["-comment_datetime"]

class TaskReview(models.Model):
    RATING_RANGE=[
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5')
    ]
    user= models.ForeignKey(UserModel, on_delete=models.CASCADE)
    task= models.ForeignKey(Task, on_delete=models.CASCADE,related_name='rates')
    rating=models.IntegerField(choices=RATING_RANGE)
    content=models.CharField(max_length=500)

    def __str__(self):
        return str(self.rating) if str(self.rating) else ''


class Book(models.Model):
    name=models.CharField(max_length=255)
    isbn_number=models.CharField(max_length=255)

    class Meta:
        db_table='book'

    def __str__(self):
        return self.name
        
class TaskAnalysis(models.Model):
    revised_due_date=models.DateTimeField(null=True,blank=True)
    task=models.ForeignKey(Task,on_delete=models.CASCADE,null=True,blank=True)
    resubmits = models.CharField(max_length=77,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return str(self.task.title)

class SubTaskAnalysis(models.Model):
    revised_due_date=models.DateTimeField(null=True,blank=True)
    subtask=models.ForeignKey(SubTask,on_delete=models.CASCADE,null=True,blank=True)
    resubmits = models.CharField(max_length=77,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return str(self.subtask.name)

@receiver(post_save,sender=Task)
def deadline_change_score_task(sender,instance,update_fields,**kwargs):
        counter=Task.objects.get(pk=instance.pk)
        # import pdb;pdb.set_trace()
        due_dates=[]
        # if counter.due_date in update_fields:
            # due_dates.append(counter.due_date)
        # print(due_dates)
        print("There are {} tasks in the system".format(counter) )


@receiver(pre_save,sender=Task)
def deadline_changes_score_task(sender,instance,update_fields,**kwargs):
        # import pdb;pdb.set_trace()
        due_dates=[]
        if not instance._state.adding:
            counter=Task.objects.get(pk=instance.pk)
            if counter.due_date != instance.due_date:
                TaskAnalysis.objects.create(revised_due_date=instance.due_date,task=instance)
            elif instance.status == 'RES':
                TaskAnalysis.objects.create(resubmits=instance.status,task=instance)
        else:
            print ('this is an insert')

@receiver(pre_save,sender=SubTask)
def deadline_change_score_subtask(sender,instance,**kwargs):
        if not instance._state.adding:
            counter=SubTask.objects.get(pk=instance.pk)
            if counter.task_due_date != instance.task_due_date:
                SubTaskAnalysis.objects.create(revised_due_date=instance.task_due_date,subtask=instance)
            elif instance.status == 'RES':
                SubTaskAnalysis.objects.create(resubmits=instance.status,subtask=instance)

        else:
            print('this is an insert')


