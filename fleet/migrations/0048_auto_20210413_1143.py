# Generated by Django 2.1.15 on 2021-04-13 11:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0047_auto_20210330_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='date_start',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date of Travel'),
        ),
    ]
