# Generated by Django 2.1.1 on 2019-02-07 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0033_auto_20190207_1137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='base_profile_leave',
            new_name='base_profile',
        ),
    ]
