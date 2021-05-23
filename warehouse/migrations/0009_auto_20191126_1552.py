# Generated by Django 2.1.1 on 2019-11-26 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_auto_20191125_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incoming',
            name='attachment',
            field=models.FileField(blank=True, upload_to='incoming_form', verbose_name='Form'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='attachment',
            field=models.FileField(blank=True, upload_to='incoming_form', verbose_name='Form'),
        ),
    ]
