from django.db.models.signals import (
    post_delete,post_init,post_migrate,post_save,
    pre_delete,pre_init,pre_migrate,pre_save
)
from django.core.signals import (
    request_finished,request_started,got_request_exception
)

from taskmanager.models import (
    Task,Team,SubTask
)

from django.dispatch import receiver,Signal




################
# task signals #
################
counter= Signal(providing_args=[])


################
# task signals #
################



@receiver(post_save,sender=Task)
def task_post_save_signal(sender,instance,**kwargs):
    print('this is the task post save signal')


@receiver(post_init,sender=Task)
def task_post_init_signal(sender,instance,**kwargs):
    print('this is the task post init signal')

@receiver(post_delete,sender=Task)
def task_post_delete_signal(sender,instance,**kwargs):
    print('this is the task post delete signal')

@receiver(post_migrate,sender=Task)
def task_post_migrate_signal(sender,instance,**kwargs):
    print('this is the task post migrate signal')

@receiver(pre_save,sender=Task)
def task_pre_save_signal(sender,instance,**kwargs):
    print('this is the task pre save signal')

@receiver(pre_init,sender=Task)
def task_pre_init_signal(sender,instance,**kwargs):
    print('this is the task post init signal')

@receiver(pre_delete,sender=Task)
def task_pre_delete_signal(sender,instance,**kwargs):
    print('this is the task post delete signal')

@receiver(pre_migrate,sender=Task)
def task_pre_migrate_signal(sender,instance,**kwargs):
    print('this is the task post migrate signal')

@receiver(request_finished)
def task_request_finished_signal(sender,**kwargs):
    print('this is the task request finished signal')

@receiver(request_started)
def task_request_started_signal(sender,**kwargs):
    print('this is the task request started signal')

@receiver(got_request_exception)
def task_got_request_exception_signal(sender,**kwargs):
    print('this is the task got request exception signal')


###################
# subtask signals #
###################
counter=Signal(providing_args=[])




################
# subtask signals #
################
@receiver(post_save,sender=SubTask)
def subtask_post_save_signal(sender,instance,**kwargs):
    print('this is the subtask post save signal')


@receiver(post_init,sender=SubTask)
def subtask_post_init_signal(sender,instance,**kwargs):
    print('this is the subtask post init signal')

@receiver(post_delete,sender=SubTask)
def subtask_post_delete_signal(sender,instance,**kwargs):
    print('this is the subtask post delete signal')

@receiver(post_migrate,sender=SubTask)
def subtask_post_migrate_signal(sender,instance,**kwargs):
    print('this is the subtask post migrate signal')

@receiver(pre_save,sender=SubTask)
def subtask_pre_save_signal(sender,instance,**kwargs):
    print('this is the subtask pre save signal')

@receiver(pre_init,sender=SubTask)
def subtask_pre_init_signal(sender,instance,**kwargs):
    print('this is the subtask pre init signal')

@receiver(pre_delete,sender=SubTask)
def subtask_pre_delete_signal(sender,instance,**kwargs):
    print('this is the subtask pre delete signal')

@receiver(pre_migrate,sender=SubTask)
def subtask_pre_migrate_signal(sender,instance,**kwargs):
    print('this is the subtask pre migrate signal')

@receiver(request_finished)
def subtask_request_finished_signal(sender,**kwargs):
    print('this is the subtask request finished signal')

@receiver(request_started)
def subtask_request_started_signal(sender,**kwargs):
    print('this is the subtask request started signal')

@receiver(got_request_exception)
def subtask_got_request_exception_signal(sender,**kwargs):
    print('this is the subtask got request exception signal')



################
# team signals #
################
counter=Signal(providing_args=[])

################
# team signals #
################
@receiver(post_save,sender=Team)
def team_post_save_signal(sender,instance,**kwargs):
    print('this is the team post save signal')


@receiver(post_init,sender=Team)
def team_post_init_signal(sender,instance,**kwargs):
    print('this is the team post init signal')

@receiver(post_delete,sender=Team)
def team_post_delete_signal(sender,instance,**kwargs):
    print('this is the team post delete signal')

@receiver(post_migrate,sender=Team)
def team_post_migrate_signal(sender,instance,**kwargs):
    print('this is the team post migrate signal')

@receiver(pre_save,sender=Team)
def team_pre_save_signal(sender,instance,**kwargs):
    print('this is the team pre save signal')

@receiver(pre_init,sender=Team)
def team_pre_init_signal(sender,instance,**kwargs):
    print('this is the team pre init signal')

@receiver(pre_delete,sender=Team)
def team_pre_delete_signal(sender,instance,**kwargs):
    print('this is the team pre delete signal')

@receiver(pre_migrate,sender=Team)
def team_pre_migrate_signal(sender,instance,**kwargs):
    print('this is the team pre migrate signal')

@receiver(request_finished)
def team_request_finished_signal(sender,**kwargs):
    print('this is the team request finished signal')

@receiver(request_started)
def team_request_started_signal(sender,**kwargs):
    print('this is the team request started signal')

@receiver(got_request_exception)
def team_got_request_exception_signal(sender,**kwargs):
    print('this is the team got request exception signal')
