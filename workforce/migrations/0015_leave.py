# Generated by Django 2.1.1 on 2018-11-09 09:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0014_auto_20181028_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(verbose_name='Start Date')),
                ('date_to', models.DateField(verbose_name='Start End')),
                ('leave_type', models.CharField(choices=[('Birthday Leave', 'Birthday Leave'), ('For Approval', 'For Approval'), ('Denied', 'Denied'), ('Canceled', 'Canceled')], max_length=200, verbose_name='Status')),
                ('reason', models.CharField(max_length=500, verbose_name='Reason')),
                ('approval', models.CharField(choices=[('Approved', 'Approved'), ('For Approval', 'For Approval'), ('Denied', 'Denied'), ('Canceled', 'Canceled')], default='For Approval', max_length=200, verbose_name='Status')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to='workforce.BasicProfile')),
                ('base_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave', to='workforce.BasicProfile')),
            ],
            options={
                'verbose_name': 'Leave Monitoring',
                'verbose_name_plural': 'Leave Monitoring',
            },
        ),
    ]
