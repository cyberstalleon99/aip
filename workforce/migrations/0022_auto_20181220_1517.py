# Generated by Django 2.1.1 on 2018-12-20 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0021_auto_20181220_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='referral',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Referral'),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='regularization',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Regularization'),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='end_probation',
            field=models.DateField(blank=True, null=True, verbose_name='End of Probation'),
        ),
    ]
