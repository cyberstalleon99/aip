# Generated by Django 2.1.1 on 2018-12-14 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0024_auto_20181213_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='base_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='op_status', to='operation.Project'),
        ),
    ]