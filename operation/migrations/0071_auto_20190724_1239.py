# Generated by Django 2.1.1 on 2019-07-24 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0070_projectitem_dependency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='majorexpense',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='majorexpense',
            name='spending',
        ),
        migrations.AddField(
            model_name='majorexpense',
            name='admin',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Admin'),
        ),
        migrations.AddField(
            model_name='majorexpense',
            name='drawings',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Drawings'),
        ),
        migrations.AddField(
            model_name='majorexpense',
            name='equipment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Equipment'),
        ),
        migrations.AddField(
            model_name='majorexpense',
            name='labor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Labor'),
        ),
        migrations.AddField(
            model_name='majorexpense',
            name='materials',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Materials'),
        ),
        migrations.AddField(
            model_name='majorexpense',
            name='overhead',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Overhead'),
        ),
        migrations.AddField(
            model_name='majorexpense',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Total'),
        ),
        migrations.AddField(
            model_name='majorexpense',
            name='vat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='VAT'),
        ),
    ]