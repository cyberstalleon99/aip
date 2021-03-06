# Generated by Django 2.1.15 on 2021-03-30 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0045_auto_20210329_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='status',
            field=models.CharField(blank=True, choices=[('Scheduled', 'Scheduled'), ('Travel Booked', 'Travel Booked'), ('On its way', 'On its way'), ('Arrived', 'Arrived'), ('Coming back', 'Coming back'), ('Returned', 'Returned'), ('Canceled', 'Canceled')], default='Travel Booked', max_length=50, null=True, verbose_name='Status'),
        ),
    ]
