# Generated by Django 2.1.1 on 2019-11-14 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0004_auto_20191114_1711'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joimage',
            options={'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterField(
            model_name='joimage',
            name='base_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wo_images', to='fleet.WorkOrder'),
        ),
        migrations.AlterField(
            model_name='joimage',
            name='jo_pic',
            field=models.ImageField(blank=True, upload_to='wo_pic', verbose_name='Image'),
        ),
    ]
