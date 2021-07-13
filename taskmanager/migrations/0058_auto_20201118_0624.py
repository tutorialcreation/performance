# Generated by Django 3.0.1 on 2020-11-18 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0057_auto_20201113_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='status',
            field=models.CharField(choices=[('BID', 'Successfully Bidded'), ('NBID', 'Unsuccessful Bid'), ('PLAN', 'To Accept'), ('PROG', 'On going'), ('COMP', 'Completed'), ('RES', 'Resubmit'), ('PA', 'Pending Approval'), ('APP', 'Approved'), ('REV', 'Revise'), ('RET', 'Resubmitted'), ('INV', 'Invoiced')], default='PLAN', max_length=4, null=True),
        ),
    ]