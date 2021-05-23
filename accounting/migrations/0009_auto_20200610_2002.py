# Generated by Django 2.1.1 on 2020-06-10 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_pricelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricelist',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Price'),
        ),
    ]