# Generated by Django 2.1.1 on 2020-09-17 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workforce', '0074_auto_20200615_1144'),
        ('accounting', '0018_auto_20200916_0049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_date', models.DateField(default=django.utils.timezone.now, verbose_name='Transaction Date (Actual):')),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Quantity')),
                ('base_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trans_por', to='accounting.OrderRequest', verbose_name='POR Trans #')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': 'Entry', 'verbose_name_plural': 'Entries'},
        ),
        migrations.AddField(
            model_name='transaction',
            name='entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trans_entry', to='accounting.Entry', verbose_name='Transaction Entry'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trans_item', to='accounting.Item'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='project_site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trans_site', to='workforce.ProjectSite'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='done_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
