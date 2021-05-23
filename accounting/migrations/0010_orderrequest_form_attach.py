# Generated by Django 2.1.1 on 2020-06-15 11:44

import accounting.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_auto_20200610_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderrequest',
            name='form_attach',
            field=models.ImageField(blank=True, upload_to='po_forms', validators=[accounting.models.validate_upload_size], verbose_name='Image'),
        ),
    ]
