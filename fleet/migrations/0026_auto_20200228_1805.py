# Generated by Django 2.1.1 on 2020-02-28 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0025_auto_20200224_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joborder',
            name='status',
            field=models.CharField(choices=[('For Approval', 'For Approval'), ('Under Repair', 'Under Repair'), ('For PMS', 'For PMS'), ('Sustained', 'Sustained'), ('Finished', 'Finished')], default='For Approval', max_length=200, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='service_type',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('Unscheduled', 'Unscheduled'), ('Capital Repair', 'Capital Repair'), ('PMS', 'PMS'), ('Sustained', 'Sustained')], max_length=200, verbose_name='Type of Service'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='wo_status',
            field=models.CharField(choices=[('For Approval', 'For Approval'), ('Under Repair', 'Under Repair'), ('For PMS', 'For PMS'), ('Sustained', 'Sustained'), ('Finished', 'Finished')], default='Under Repair', max_length=200, verbose_name='Status'),
        ),
    ]
