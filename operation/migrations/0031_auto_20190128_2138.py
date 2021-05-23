# Generated by Django 2.1.1 on 2019-01-28 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0030_report_weather'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'get_latest_by': 'date', 'verbose_name': 'Report', 'verbose_name_plural': 'Reports'},
        ),
        migrations.AlterField(
            model_name='personnel',
            name='title',
            field=models.CharField(choices=[('Project Manager', 'Project Manager'), ('Project Engineer', 'Project Engineer'), ('Materials Engineer', 'Materials Engineer'), ('Resident Engineer', 'Resident Engineer'), ('Project Facilitator', 'Project Facilitator'), ('Geodetic Engineer', 'Geodetic Engineer'), ('Office Engineer', 'Office Engineer'), ('Foreman', 'Foreman'), ('Regional Technical Engineer', 'Regional Technical Engineer')], max_length=200, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='report',
            name='slippage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Slippage (%)'),
        ),
        migrations.AlterField(
            model_name='report',
            name='work_accomplished',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Work Done (%)'),
        ),
    ]
