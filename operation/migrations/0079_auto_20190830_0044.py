# Generated by Django 2.1.1 on 2019-08-29 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0078_auto_20190830_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporting',
            name='document',
            field=models.FileField(upload_to='reports_docs/', verbose_name='Upload Report'),
        ),
    ]
