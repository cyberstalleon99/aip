# Generated by Django 2.1.1 on 2020-09-18 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0022_auto_20200918_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='incoming_vat',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='vat',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='vatable_sales',
        ),
    ]