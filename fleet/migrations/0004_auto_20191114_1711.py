# Generated by Django 2.1.1 on 2019-11-14 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0003_joimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joborder',
            name='jo_pic',
        ),
        migrations.RemoveField(
            model_name='workorder',
            name='wo_pic',
        ),
    ]
