# Generated by Django 2.1.1 on 2020-03-05 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_auto_20200219_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='purchaser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchased_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
