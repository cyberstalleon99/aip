# Generated by Django 2.1.1 on 2018-12-19 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0018_auto_20181127_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_title', models.CharField(max_length=200, verbose_name='Title')),
                ('document_type', models.CharField(choices=[('Permit', 'Permit'), ('Certificate', 'Certificate'), ('License', 'License')], max_length=200, verbose_name='Document Type')),
                ('issued_date', models.DateField(verbose_name='Date Issued')),
                ('expiry_date', models.DateField(verbose_name='Expiry Date')),
                ('doc_image', models.ImageField(default='profile_pic/default.png', upload_to='doc_files', verbose_name='Scanned Document')),
            ],
            options={
                'verbose_name': 'Documents',
                'verbose_name_plural': 'Documents',
            },
        ),
    ]
