# Generated by Django 2.1.1 on 2019-11-27 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0010_auto_20191127_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='doc_file',
            field=models.FileField(blank=True, default='', null=True, upload_to='unit_files', verbose_name='Document'),
        ),
    ]
