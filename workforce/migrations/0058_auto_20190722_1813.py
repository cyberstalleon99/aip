# Generated by Django 2.1.1 on 2019-07-22 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0057_projectsite_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='attachment',
            field=models.FileField(blank=True, default=' ', upload_to='leave_files', verbose_name='Upload Leave'),
        ),
    ]
