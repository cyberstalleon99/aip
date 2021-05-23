# Generated by Django 2.1.1 on 2020-09-22 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0075_subcon'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0033_auto_20200922_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_date', models.DateField(default=django.utils.timezone.now, verbose_name='Transaction Date (Actual):')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount')),
                ('remarks', models.TextField(verbose_name='Remarks')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request_modified_by', to=settings.AUTH_USER_MODEL)),
                ('project_site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request_project_site', to='workforce.ProjectSite')),
                ('request_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request_from', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fund Request',
                'verbose_name_plural': 'Fund Requests',
            },
        ),
    ]
