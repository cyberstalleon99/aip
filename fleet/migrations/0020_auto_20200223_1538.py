# Generated by Django 2.1.1 on 2020-02-23 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0019_auto_20200222_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='document_title',
        ),
        migrations.AlterField(
            model_name='attachment',
            name='document_type',
            field=models.CharField(choices=[('OR', 'OR'), ('CR', 'CR'), ('Deed of Sale', 'Deed of Sale'), ('Certificate', 'Certificate'), ('Violations', 'Violations'), ('Technical Specs', 'Technical Specs')], max_length=200, verbose_name='Document Type'),
        ),
    ]
