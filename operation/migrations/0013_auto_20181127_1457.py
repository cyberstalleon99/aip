# Generated by Django 2.1.1 on 2018-11-27 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0012_remove_workpercentage_value2'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WorkPercentage',
            new_name='ActualWork',
        ),
    ]
