# Generated by Django 2.2 on 2020-09-21 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskmanager', '0046_auto_20200910_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='accepted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accepted_subtasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PLAN', 'Begin'), ('PROG', 'On going'), ('COMP', 'Completed'), ('RES', 'Resubmit'), ('PA', 'Pending Approval'), ('APP', 'Approved'), ('REV', 'Revise'), ('RET', 'Resubmitted'), ('iNV', 'Invoiced')], default='PLAN', max_length=4, null=True),
        ),
    ]
