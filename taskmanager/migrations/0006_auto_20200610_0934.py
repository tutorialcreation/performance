# Generated by Django 3.0.7 on 2020-06-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0005_auto_20200610_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='revised_due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PLAN', 'To Accept'), ('PROG', 'On going'), ('COMP', 'Completed'), ('APP', 'Approved'), ('REV', 'Revise')], default='PLAN', max_length=4),
        ),
    ]
