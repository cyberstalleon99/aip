# Generated by Django 2.1.1 on 2019-01-29 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0035_auto_20190129_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='weather',
            field=models.CharField(choices=[('Sunny', 'Sunny'), ('Cloudy', 'Cloudy'), ('Rainy', 'Rainy'), ('Windy', 'Windy'), ('Stormy', 'Stormy')], default='Sunny', max_length=200, verbose_name='Weather Condition'),
        ),
    ]
