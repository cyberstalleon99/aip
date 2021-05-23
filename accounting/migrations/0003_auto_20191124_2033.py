# Generated by Django 2.1.1 on 2019-11-24 20:33

import accounting.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20190906_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashbudget',
            name='doc_file',
            field=models.FileField(blank=True, upload_to='cf_files', validators=[accounting.models.validate_upload_size], verbose_name='Form'),
        ),
    ]