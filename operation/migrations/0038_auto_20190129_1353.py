# Generated by Django 2.1.1 on 2019-01-29 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0037_auto_20190129_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.CharField(choices=[('For Bidding', 'For Bidding'), ('Under Construction', 'Under Construction'), ('Completed', 'Completed')], default='Under Construction', max_length=200, verbose_name='Status'),
        ),
    ]