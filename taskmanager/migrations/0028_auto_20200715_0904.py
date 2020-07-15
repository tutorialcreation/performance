# Generated by Django 3.0.7 on 2020-07-15 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0027_subtask_revised_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='content',
            field=models.CharField(max_length=500, null=True, verbose_name='comments'),
        ),
        migrations.AddField(
            model_name='subtask',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
    ]
