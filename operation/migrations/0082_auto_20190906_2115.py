# Generated by Django 2.1.1 on 2019-09-06 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0081_auto_20190906_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workstat',
            name='actual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Actual Value'),
        ),
        migrations.AlterField(
            model_name='workstat',
            name='planned',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Planned Value'),
        ),
        migrations.AlterField(
            model_name='workstat',
            name='slippage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Slippage'),
        ),
    ]
