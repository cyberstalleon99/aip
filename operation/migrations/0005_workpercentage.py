# Generated by Django 2.1.1 on 2018-11-27 11:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_auto_20181127_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkPercentage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('work_type', models.CharField(choices=[('As Planned', 'As Planned'), ('Actual', 'Actual')], max_length=200, verbose_name='Type')),
                ('value', models.DecimalField(decimal_places=0, default=0, max_digits=20, verbose_name='Value')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('base_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='percentage', to='operation.Project')),
            ],
            options={
                'verbose_name': 'Work Accomplished',
                'verbose_name_plural': 'Work Accomplished',
            },
        ),
    ]