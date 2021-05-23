# Generated by Django 2.1.1 on 2020-02-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0066_auto_20200209_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicprofile',
            name='mobile2',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20, verbose_name='Globe'),
        ),
        migrations.AlterField(
            model_name='basicprofile',
            name='mobile',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=20, verbose_name='Smart'),
        ),
    ]