# Generated by Django 2.1.1 on 2019-08-02 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0059_auto_20190723_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectsite',
            name='project_code',
            field=models.CharField(db_index=True, max_length=40, verbose_name='Project Code'),
        ),
    ]
