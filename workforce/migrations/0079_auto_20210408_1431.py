# Generated by Django 2.1.15 on 2021-04-08 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0078_basicprofile_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicprofile',
            name='mobile',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20, verbose_name='Primary'),
        ),
        migrations.AlterField(
            model_name='basicprofile',
            name='mobile2',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20, verbose_name='Secondary'),
        ),
    ]