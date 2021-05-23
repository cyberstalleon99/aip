# Generated by Django 2.1.1 on 2020-09-23 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0037_entry_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='incoming_vat',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=20, verbose_name='Vat'),
        ),
        migrations.AddField(
            model_name='entry',
            name='vat',
            field=models.BooleanField(default=False, verbose_name='Vatable?'),
        ),
        migrations.AddField(
            model_name='entry',
            name='vatable_sales',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=20, verbose_name='Vatable Sales'),
            preserve_default=False,
        ),
    ]