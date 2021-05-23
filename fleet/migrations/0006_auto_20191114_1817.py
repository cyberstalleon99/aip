# Generated by Django 2.1.1 on 2019-11-14 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0005_auto_20191114_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joimage',
            name='base_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jo_images', to='fleet.JobOrder'),
        ),
        migrations.AlterField(
            model_name='joimage',
            name='jo_pic',
            field=models.ImageField(blank=True, upload_to='jo_pic', verbose_name='Image'),
        ),
    ]
