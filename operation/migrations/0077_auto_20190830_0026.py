# Generated by Django 2.1.1 on 2019-08-29 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0076_auto_20190830_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporting',
            name='document',
            field=models.FileField(default='', upload_to='reports_docs/', verbose_name='Upload Report'),
        ),
    ]