# Generated by Django 2.1.1 on 2019-09-06 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0082_auto_20190906_2115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'get_latest_by': 'date', 'verbose_name': 'Daily Report', 'verbose_name_plural': 'Daily Reports'},
        ),
    ]