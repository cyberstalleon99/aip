# Generated by Django 2.1.1 on 2019-03-18 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0049_auto_20190308_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='attachment',
            field=models.ImageField(blank=True, default='profile_pic/default.png', upload_to='leave_files', verbose_name='Upload Leave'),
        ),
    ]
