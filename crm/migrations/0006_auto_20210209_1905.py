# Generated by Django 3.0.1 on 2021-02-09 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20210209_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='price',
            field=models.CharField(blank=True, max_length=1200, null=True),
        ),
    ]
