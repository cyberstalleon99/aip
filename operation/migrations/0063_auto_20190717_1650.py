# Generated by Django 2.1.1 on 2019-07-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0062_auto_20190717_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workstat',
            name='date_start',
            field=models.DateField(blank=True, null=True, verbose_name='Start Date'),
        ),
    ]
