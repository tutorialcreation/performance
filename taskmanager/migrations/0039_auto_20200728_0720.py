# Generated by Django 3.0.7 on 2020-07-28 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0038_auto_20200728_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtaskanalysis',
            name='resubmits',
            field=models.CharField(blank=True, max_length=77, null=True),
        ),
        migrations.AlterField(
            model_name='taskanalysis',
            name='resubmits',
            field=models.CharField(blank=True, max_length=77, null=True),
        ),
    ]
