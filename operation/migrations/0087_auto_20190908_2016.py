# Generated by Django 2.1.1 on 2019-09-08 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0086_auto_20190907_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.CharField(choices=[('For Bidding', 'For Bidding'), ('Under Construction', 'Under Construction'), ('Completed', 'Completed'), ('Warehouse', 'Warehouse')], default='Under Construction', max_length=200, verbose_name='Status'),
        ),
    ]
