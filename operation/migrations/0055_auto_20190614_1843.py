# Generated by Django 2.1.1 on 2019-06-14 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0054_auto_20190614_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_pic',
            field=models.ImageField(default='profile_pic/default.png', upload_to='project_pic', verbose_name='Project Profile'),
        ),
    ]