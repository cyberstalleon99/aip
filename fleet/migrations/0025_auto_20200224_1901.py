# Generated by Django 2.1.1 on 2020-02-24 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0024_auto_20200224_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Description'),
        ),
    ]
