# Generated by Django 3.1 on 2020-08-10 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0041_auto_20200809_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='status',
            field=models.CharField(choices=[('PLAN', 'To Accept'), ('PROG', 'On going'), ('COMP', 'Completed'), ('RES', 'Resubmit'), ('PA', 'Pending Approval'), ('APP', 'Approved'), ('REV', 'Revise'), ('RET', 'Resubmitted')], default='PLAN', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PLAN', 'To Accept'), ('PROG', 'On going'), ('COMP', 'Completed'), ('RES', 'Resubmit'), ('PA', 'Pending Approval'), ('APP', 'Approved'), ('REV', 'Revise'), ('RET', 'Resubmitted')], default='PLAN', max_length=4, null=True),
        ),
    ]