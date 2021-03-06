# Generated by Django 2.1.1 on 2020-09-18 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workforce', '0074_auto_20200615_1144'),
        ('accounting', '0025_auto_20200918_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='detail',
            field=models.TextField(default=0, verbose_name='Remarks'),
            preserve_default=False,
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
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Quantity'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trans_supplier', to='accounting.Supplier'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='trans_type',
            field=models.CharField(choices=[('Debit', 'Debit'), ('Adjustment', 'Adjustment'), ('Credit', 'Credit')], default='Debit', max_length=200, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='done_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
