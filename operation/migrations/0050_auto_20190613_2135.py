# Generated by Django 2.1.1 on 2019-06-13 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0049_auto_20190613_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Facilities for Engineers', 'Facilities for Engineers'), ('Other General Requirements', 'Other General Requirements'), ('Earth Works', 'Earth Works'), ('Sub Base and Base Course', 'Sub Base and Base Course'), ('Surface Course', 'Surface Course'), ('Drainage and Slope Protection', 'Drainage and Slope Protection'), ('Miscellaneous', 'Miscellaneous')], max_length=200, verbose_name='Category'),
        ),
    ]