# Generated by Django 2.1.1 on 2020-09-23 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0035_fundrequest_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='transaction_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trans_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
