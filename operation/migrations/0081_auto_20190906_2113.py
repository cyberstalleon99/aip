# Generated by Django 2.1.1 on 2019-09-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0080_auto_20190906_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workstat',
            name='slippage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Slippage'),
        ),
    ]