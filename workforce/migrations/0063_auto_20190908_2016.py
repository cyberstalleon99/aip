# Generated by Django 2.1.1 on 2019-09-08 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0062_auto_20190815_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsite',
            name='project_type',
            field=models.CharField(choices=[('Office', 'Office'), ('Project', 'Project'), ('Warehouse', 'Warehouse'), ('Quary', 'Quary')], default='Project', max_length=200, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='projectsite',
            name='project_status',
            field=models.CharField(choices=[('For Bidding', 'For Bidding'), ('Under Construction', 'Under Construction'), ('Completed', 'Completed'), ('Warehouse', 'Warehouse')], default='Completed', max_length=200, verbose_name='Status'),
        ),
    ]