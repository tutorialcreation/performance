# Generated by Django 3.0.7 on 2020-07-13 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0024_subtask_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='team_leader',
            field=models.BooleanField(default=False),
        ),
    ]
