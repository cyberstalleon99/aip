# Generated by Django 2.1.1 on 2019-06-13 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0043_workstat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actualwork',
            name='base_project',
        ),
        migrations.RemoveField(
            model_name='plannedwork',
            name='base_project',
        ),
        migrations.DeleteModel(
            name='ActualWork',
        ),
        migrations.DeleteModel(
            name='PlannedWork',
        ),
    ]