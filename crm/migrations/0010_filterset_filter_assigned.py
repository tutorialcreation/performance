# Generated by Django 3.0.1 on 2021-02-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_filterset'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterset',
            name='filter_assigned',
            field=models.CharField(blank=True, choices=[('A', 'All'), ('ACO', 'All Contact Persons'), ('ACL', 'All Clients'), ('CC', 'Client Country'), ('CL', 'Client Location'), ('CP', 'Client Postal Address'), ('CS', 'Client Status'), ('CN', 'Client Name'), ('CT', 'Client Telephone'), ('CE', 'Client Email'), ('CPN', 'Contact Person Name'), ('CPP', 'Contact Person Position'), ('CPT', 'Contact Person Telephone'), ('CPE', 'Contact Person Email'), ('CPS', 'Contact Person Status'), ('CPC', 'Contact Person Client'), ('CPSE', 'Contact Person ServiceLine'), ('UE', 'Use Existing Filters')], max_length=200, null=True),
        ),
    ]
