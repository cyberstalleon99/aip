# Generated by Django 2.1.1 on 2020-09-23 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0036_auto_20200923_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='attachment',
            field=models.FileField(blank=True, default='', upload_to='entry_files', verbose_name='Attachment'),
        ),
    ]
