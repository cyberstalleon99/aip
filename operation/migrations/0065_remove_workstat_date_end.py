# Generated by Django 2.1.1 on 2019-07-17 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0064_workstat_date_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workstat',
            name='date_end',
        ),
    ]