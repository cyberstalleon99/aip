# Generated by Django 2.1.1 on 2018-11-27 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0015_majorexpense'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationalcost',
            name='base_project',
        ),
        migrations.DeleteModel(
            name='OperationalCost',
        ),
    ]