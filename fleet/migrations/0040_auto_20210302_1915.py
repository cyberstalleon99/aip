# Generated by Django 2.1.1 on 2021-03-02 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0039_auto_20210302_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='note',
            field=models.TextField(verbose_name='Details'),
        ),
    ]