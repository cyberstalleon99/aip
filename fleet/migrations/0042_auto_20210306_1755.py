# Generated by Django 2.1.15 on 2021-03-06 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0041_auto_20210304_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='document_type',
            field=models.CharField(choices=[('OR', 'OR'), ('CR', 'CR'), ('Deed of Sale', 'Deed of Sale'), ('Certificate', 'Certificate'), ('Violations', 'Violations'), ('Technical Specs', 'Technical Specs'), ('Turn Over Forms', 'Turn Over Forms'), ('Inspection Checklist', 'Inspection Checklist'), ('Transmittal Form', 'Transmittal Form'), ('Incident Report', 'Incident Report')], max_length=200, verbose_name='Document Type'),
        ),
        migrations.AlterField(
            model_name='travel',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('In Transit', 'In Transit'), ('Arrived', 'Arrived'), ('Canceled', 'Canceled')], default='Travel Booked', max_length=50, verbose_name='Status'),
        ),
    ]
