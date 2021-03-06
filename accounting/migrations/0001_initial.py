# Generated by Django 2.1.1 on 2019-09-03 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workforce', '0062_auto_20190815_2012'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_type', models.CharField(choices=[('Cash In', 'Cash In'), ('Cash Out', 'Cash Out')], default='Cash Out', max_length=200, verbose_name='Transaction')),
                ('trans_date', models.DateField(default=django.utils.timezone.now, verbose_name='Transaction Date:')),
                ('form_no', models.CharField(max_length=10, verbose_name='Form No.')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount')),
                ('detail', models.CharField(max_length=200, verbose_name='Detail')),
                ('doc_file', models.FileField(blank=True, default=' ', upload_to='cf_files', verbose_name='Form')),
                ('cdv_date', models.DateField(default=django.utils.timezone.now, verbose_name='CDV Date:')),
                ('cdv_no', models.CharField(default='0', max_length=10, verbose_name='CDV No.')),
                ('status', models.CharField(choices=[('Unliquidated', 'Unliquidated'), ('For Review', 'For Review'), ('Verified', 'Verified')], default='Unliquidated', max_length=200, verbose_name='Audit 1')),
                ('status2', models.CharField(choices=[('Unliquidated', 'Unliquidated'), ('For Review', 'For Review'), ('Verified', 'Verified')], default='For Review', max_length=200, verbose_name='Audit 2')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('issued_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cs_issued_by', to=settings.AUTH_USER_MODEL)),
                ('issued_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cs_issued_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cash Fund',
                'verbose_name_plural': 'Cash Fund',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200, verbose_name='Name')),
                ('general_name', models.CharField(max_length=200, verbose_name='Class Name')),
                ('item_category', models.CharField(choices=[('Construction Materials', 'Construction Materials'), ('Spare Parts', 'Spare Parts'), ('Oil & Lubricants', 'Oil & Lubricants'), ('PPE', 'PPE'), ('Tools & Machineries', 'Tools & Machineries'), ('Office Supply', 'Office Supply'), ('Food Supply', 'Food Supply'), ('Fuel', 'Fuel'), ('Kitchen Utensils', 'Kitchen Utensils')], max_length=200, verbose_name='Category')),
                ('item_unit', models.CharField(max_length=200, verbose_name='Unit')),
                ('item_detail', models.TextField(verbose_name='Detail')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='ItemCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=10, verbose_name='Code')),
                ('sc1', models.CharField(default='', max_length=200, verbose_name='General Ledger Account')),
                ('sc2', models.CharField(blank=True, default='', max_length=200, verbose_name='Subsidiary Ledger Account 1')),
                ('sc3', models.CharField(blank=True, default='', max_length=200, verbose_name='Subsidiary Ledger Account 2')),
            ],
            options={
                'verbose_name': 'Chart of Account',
                'verbose_name_plural': 'Chart of Accounts',
            },
        ),
        migrations.CreateModel(
            name='Liquidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_date', models.DateField(default=django.utils.timezone.now, verbose_name='___Transaction Date:___')),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Quantity')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount')),
                ('detail', models.CharField(max_length=200, verbose_name='Detail')),
                ('payment', models.CharField(choices=[('Cash', 'Cash'), ('Credit', 'Credit')], default='Cash', max_length=200, verbose_name='Payment Mode')),
                ('category', models.CharField(choices=[('Uncategorized', 'Uncategorized'), ('Materials', 'Materials'), ('Labor', 'Labor'), ('General & Admin', 'General & Admin'), ('Overhead', 'Overhead')], default='Uncategorized', max_length=200, verbose_name='Account Category')),
                ('trans_type', models.CharField(choices=[('Debit', 'Debit'), ('Adjustment', 'Adjustment'), ('Credit', 'Credit')], default='Debit', max_length=200, verbose_name='Type')),
                ('incoming_vat', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=20, verbose_name='Vat')),
                ('vatable_sales', models.DecimalField(decimal_places=2, editable=False, max_digits=20, verbose_name='Vatable Sales')),
                ('vat', models.BooleanField(default=False, verbose_name='Vatable?')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('base_budget', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liquidation', to='accounting.CashBudget', verbose_name='CRS #')),
            ],
            options={
                'verbose_name': 'Liquidation',
                'verbose_name_plural': 'Liquidations',
            },
        ),
        migrations.CreateModel(
            name='OrderRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date')),
                ('request_form', models.CharField(default=0, max_length=50, verbose_name='POR No')),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Quantity')),
                ('details', models.TextField(default='Details here...', verbose_name='Details')),
                ('status', models.CharField(choices=[('For Approval', 'For Approval'), ('On-Process', 'On-Process'), ('Purchased', 'Purchased'), ('Canceled', 'Canceled')], default='For Approval', max_length=200, verbose_name='Status')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_request', to='accounting.Item')),
                ('project_site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='or_project_site', to='workforce.ProjectSite')),
                ('purchaser', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchased_by', to=settings.AUTH_USER_MODEL)),
                ('request_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='or_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Item Request',
                'verbose_name_plural': 'Item Request',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('address', models.CharField(max_length=200, verbose_name='Address')),
                ('contact', models.CharField(max_length=200, verbose_name='Contact')),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
            },
        ),
        migrations.AddField(
            model_name='liquidation',
            name='base_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='por', to='accounting.OrderRequest', verbose_name='POR #'),
        ),
        migrations.AddField(
            model_name='liquidation',
            name='issued_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issued_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='liquidation',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item', to='accounting.Item'),
        ),
        migrations.AddField(
            model_name='liquidation',
            name='item_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_liquidation', to='accounting.ItemCode'),
        ),
        migrations.AddField(
            model_name='liquidation',
            name='project_site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='liquidation_project_site', to='workforce.ProjectSite'),
        ),
        migrations.AddField(
            model_name='liquidation',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplier', to='accounting.Supplier'),
        ),
    ]
