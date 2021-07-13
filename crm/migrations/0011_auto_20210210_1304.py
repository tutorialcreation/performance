# Generated by Django 3.0.1 on 2021-02-10 13:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_filterset_filter_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filterset',
            name='filter_assigned',
            field=models.CharField(blank=True, choices=[('A', 'All'), ('ACO', 'All Contact Persons'), ('ACL', 'All Clients'), ('CC', 'Client Country'), ('CL', 'Client Location'), ('CP', 'Client Postal Address'), ('CS', 'Client Status'), ('CN', 'Client Name'), ('CT', 'Client Telephone'), ('CE', 'Client Email'), ('CPN', 'Contact Person Name'), ('CPP', 'Contact Person Position'), ('CPT', 'Contact Person Telephone'), ('CPE', 'Contact Person Email'), ('CPS', 'Contact Person Status'), ('CPC', 'Contact Person Client'), ('CPSE', 'Contact Person ServiceLine'), ('UE', 'Use Existing Filters')], max_length=200, null=True, verbose_name='Which filter(s) do you want to assign ??. '),
        ),
        migrations.AlterField(
            model_name='filterset',
            name='filtered_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=2048, null=True), blank=True, null=True, size=None),
        ),
    ]