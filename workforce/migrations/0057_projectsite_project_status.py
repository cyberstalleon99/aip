# Generated by Django 2.1.1 on 2019-07-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0056_auto_20190614_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsite',
            name='project_status',
            field=models.CharField(choices=[('For Bidding', 'For Bidding'), ('Under Construction', 'Under Construction'), ('Completed', 'Completed')], default='Completed', max_length=200, verbose_name='Status'),
        ),
    ]