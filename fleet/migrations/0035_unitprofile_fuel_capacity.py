# Generated by Django 2.1.1 on 2021-01-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0034_auto_20200421_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitprofile',
            name='fuel_capacity',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20, verbose_name='Fuel Capacity.'),
        ),
    ]
