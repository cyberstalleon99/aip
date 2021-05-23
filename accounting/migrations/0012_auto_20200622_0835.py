# Generated by Django 2.1.1 on 2020-06-22 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0011_orderrequest_jo_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liquidation',
            name='base_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='por', to='accounting.OrderRequest', verbose_name='POR Trans #'),
        ),
    ]
