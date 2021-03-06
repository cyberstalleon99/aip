# Generated by Django 2.1.1 on 2019-07-23 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0058_auto_20190722_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='employment_status',
            field=models.CharField(choices=[('Active', 'Active'), ('Resigned', 'Resigned'), ('Secret', 'Secret')], max_length=40, verbose_name='Employment Status'),
        ),
        migrations.AlterField(
            model_name='loans',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Denied', 'Denied'), ('Canceled', 'Canceled')], default='For Approval', max_length=200, verbose_name='Status'),
        ),
    ]
