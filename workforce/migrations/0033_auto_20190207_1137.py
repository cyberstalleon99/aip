# Generated by Django 2.1.1 on 2019-02-07 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0032_auto_20190207_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='base_profile',
            new_name='base_profile_leave',
        ),
    ]