# Generated by Django 2.1.1 on 2019-03-23 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0040_slides'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='image',
        ),
    ]
