# Generated by Django 3.0.1 on 2021-02-10 12:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20210210_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_parameter', models.CharField(blank=True, max_length=2048, null=True)),
                ('filtered_list', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=2048, null=True), blank=True, size=None)),
            ],
        ),
    ]
