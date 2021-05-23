# Generated by Django 2.1.1 on 2019-11-14 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0002_auto_20191113_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='JOImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('jo_pic', models.ImageField(blank=True, upload_to='jo_pic', verbose_name='Image')),
                ('base_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jo_images', to='fleet.JobOrder')),
            ],
            options={
                'verbose_name': 'JO/WO Image',
                'verbose_name_plural': 'JO/WO Images',
            },
        ),
    ]
