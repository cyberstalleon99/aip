# Generated by Django 2.1.1 on 2019-09-03 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workforce', '0062_auto_20190815_2012'),
        ('fleet', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Date')),
                ('form_no', models.CharField(db_index=True, default=0, max_length=20, verbose_name='FORM No')),
                ('trans_no', models.CharField(db_index=True, default=0, max_length=20, verbose_name='Tracking No')),
                ('quantity', models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=20, verbose_name='Quantity')),
                ('details', models.TextField(default='Details here...', verbose_name='Details')),
                ('attachment', models.FileField(blank=True, default=' ', upload_to='incoming_form', verbose_name='Form')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Unit Price')),
                ('status', models.CharField(choices=[('For Verification', 'For Verification'), ('Verified', 'Verified')], default='For Verification', max_length=200, verbose_name='Status')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_in', to='accounting.Item')),
                ('project_site', models.ForeignKey(default=7, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_project_site', to='workforce.ProjectSite')),
                ('received_by', models.ForeignKey(default=32, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_received_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Incoming',
                'verbose_name_plural': 'Incomings',
            },
        ),
        migrations.CreateModel(
            name='Outgoing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_date', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('trans_type', models.CharField(choices=[('Outgoing', 'Outgoing'), ('Transfer', 'Transfer')], max_length=50, verbose_name='Type')),
                ('form_no', models.CharField(default=0, max_length=20, verbose_name='FORM No')),
                ('quantity', models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=20, verbose_name='Quantity')),
                ('details', models.CharField(default='', max_length=200, verbose_name='Details')),
                ('attachment', models.FileField(blank=True, default=' ', upload_to='incoming_form', verbose_name='Form')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('base_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out', to='warehouse.Incoming')),
                ('project_site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out_project_site', to='workforce.ProjectSite')),
                ('released_by', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out_released_by', to=settings.AUTH_USER_MODEL)),
                ('released_out', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outsider_released_to', to='workforce.Outsider')),
                ('released_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out_released_to', to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_unit', to='fleet.UnitProfile')),
            ],
            options={
                'verbose_name': 'Outgoing',
                'verbose_name_plural': 'Outgoings',
            },
        ),
    ]
