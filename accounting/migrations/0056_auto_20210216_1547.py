# Generated by Django 2.1.1 on 2021-02-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0055_auto_20210215_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='approved_at',
            field=models.DateTimeField(blank=True),
        ),
    ]
