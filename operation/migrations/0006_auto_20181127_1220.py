# Generated by Django 2.1.1 on 2018-11-27 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_workpercentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workpercentage',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Value'),
        ),
    ]
