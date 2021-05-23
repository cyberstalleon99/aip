# Generated by Django 2.1.1 on 2020-02-09 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0065_filedocument_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedocument',
            name='remarks',
            field=models.CharField(default='', max_length=200, verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='filedocument',
            name='status',
            field=models.CharField(choices=[('Documents', 'Documents'), ('Processing', 'Processing'), ('Renewed', 'Renewed')], default='', max_length=50, verbose_name='Status'),
        ),
    ]
