# Generated by Django 3.0.1 on 2020-10-27 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskmanager', '0052_auto_20201025_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='return_reason',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='member_assigned',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee_subtask', to=settings.AUTH_USER_MODEL, verbose_name='Assign to:'),
        ),
    ]
