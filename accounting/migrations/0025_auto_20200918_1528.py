# Generated by Django 2.1.1 on 2020-09-18 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0024_auto_20200918_1459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='entry',
            new_name='base_entry',
        ),
    ]