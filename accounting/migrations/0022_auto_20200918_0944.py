# Generated by Django 2.1.1 on 2020-09-18 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0021_auto_20200918_0737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='remarks',
            new_name='detail',
        ),
    ]