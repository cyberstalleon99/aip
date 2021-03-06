# Generated by Django 2.1.1 on 2019-02-16 02:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0042_auto_20190216_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workhistory',
            name='end_year',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='End Year'),
        ),
        migrations.AlterField(
            model_name='workhistory',
            name='start_year',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Start Year'),
        ),
    ]
