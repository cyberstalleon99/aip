# Generated by Django 2.1.1 on 2021-03-02 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0035_unitprofile_fuel_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='create_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Created'),
        ),
        migrations.AddField(
            model_name='travel',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('In Transit', 'In Transit'), ('Arrived', 'Arrived'), ('Canceled', 'Canceled')], default='Scheduled', max_length=50, verbose_name='Status'),
        ),
    ]