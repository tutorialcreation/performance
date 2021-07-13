# Generated by Django 3.0.1 on 2021-02-10 14:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_auto_20210210_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filterset',
            name='filters_assigned',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('A', 'All'), ('ACP', 'All Contact Persons'), ('AC', 'All Clients'), ('CC', 'Client Country'), ('CL', 'Client Location'), ('CP', 'Client Postal Address'), ('CS', 'Client Status'), ('CN', 'Client Name'), ('CT', 'Client Telephone'), ('CE', 'Client Email'), ('CPN', 'Contact Person Name'), ('CPP', 'Contact Person Position'), ('CPT', 'Contact Person Telephone'), ('CPE', 'Contact Person Email'), ('CPS', 'Contact Person Status'), ('CPC', 'Contact Person Client'), ('CPSE', 'Contact Person ServiceLine'), ('UE', 'Use Existing Filters')], max_length=200, null=True, verbose_name='Which filter(s) do you want to assign ??. '), blank=True, null=True, size=None),
        ),
    ]