# Generated by Django 2.1.1 on 2019-07-24 06:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0072_auto_20190724_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllocatedExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('materials', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Materials')),
                ('equipment', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Equipment')),
                ('labor', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Labor')),
                ('overhead', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Overhead')),
                ('admin', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Admin')),
                ('drawings', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Drawings')),
                ('vat', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='VAT')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Total')),
                ('document', models.FileField(default=' ', upload_to='major_expense/', verbose_name='Document')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('base_project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allocated_expense', to='operation.Project')),
            ],
            options={
                'verbose_name': 'Allocated Expense',
                'verbose_name_plural': 'Allocated Expense',
                'get_latest_by': 'date',
            },
        ),
        migrations.AlterModelOptions(
            name='majorexpense',
            options={'get_latest_by': 'date', 'verbose_name': 'Actual Expense', 'verbose_name_plural': 'Actual Expense'},
        ),
    ]
