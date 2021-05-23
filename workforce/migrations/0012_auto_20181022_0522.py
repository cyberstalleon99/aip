# Generated by Django 2.1.1 on 2018-10-22 05:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0011_auto_20181015_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=200, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='basicprofile',
            name='home_address',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Home Address'),
        ),
        migrations.AlterField(
            model_name='basicprofile',
            name='mobile',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True, verbose_name='Mobile No.'),
        ),
        migrations.AlterField(
            model_name='basicprofile',
            name='religion',
            field=models.CharField(choices=[('Christianity', 'Christianity'), ('Pagano', 'Pagano'), ('Muslim', 'Muslim')], max_length=200, verbose_name='Religion'),
        ),
        migrations.AlterField(
            model_name='basicprofile',
            name='title',
            field=models.CharField(choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Engr.', 'Engr.'), ('Arch.', 'Arch.')], max_length=200, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='designation',
            field=models.CharField(choices=[('Driver', 'Driver'), ('Operator', 'Operator'), ('Site Checker', 'Site Checker'), ('Skilled Laborers', 'Skilled Laborers'), ('Foreman', 'Foreman'), ('Project Engineer', 'Project Engineer'), ('Office Engineer', 'Office Engineer'), ('Administrative Clerk', 'Administrative Clerk'), ('Book Keeper', 'Book Keeper'), ('Accountant', 'Accountant'), ('Finance Manager', 'Finance Manager'), ('Purchaser', 'Purchaser'), ('Helper', 'Helper'), ('Project In Charge', 'Project In Charge'), ('Liason', 'Liason'), ('Mechanical Engineer', 'Mechanical Engineer'), ('Dispatcher', 'Dispatcher'), ('Welder', 'Welder'), ('Inventory Analyst', 'Inventory Analyst'), ('Materials & Control Officer', 'Materials & Control Officer')], max_length=200, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='end_probation',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='End of Probation'),
        ),
    ]