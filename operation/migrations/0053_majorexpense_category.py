# Generated by Django 2.1.1 on 2019-06-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0052_auto_20190613_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='majorexpense',
            name='category',
            field=models.CharField(choices=[('Cement', 'Cement'), ('Labor', 'Labor'), ('Fuel', 'Fuel'), ('Materials', 'Materials'), ('Overhead', 'Overhead')], default='Labor', max_length=200, verbose_name='Category'),
            preserve_default=False,
        ),
    ]
