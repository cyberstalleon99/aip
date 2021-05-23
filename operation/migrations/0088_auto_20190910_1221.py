# Generated by Django 2.1.1 on 2019-09-10 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0087_auto_20190908_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.CharField(choices=[('For Bidding', 'For Bidding'), ('Under Construction', 'Under Construction'), ('Completed', 'Completed')], default='Under Construction', max_length=200, verbose_name='Status'),
        ),
    ]
