# Generated by Django 3.0.1 on 2021-03-03 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_auto_20210212_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmanager',
            name='contract_period',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='clientmanager',
            name='final_proposal_amounts',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='clientmanager',
            name='nature_of_assignment',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
