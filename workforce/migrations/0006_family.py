# Generated by Django 2.1.1 on 2018-10-14 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0005_accounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Name')),
                ('relation', models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Sibling', 'Sibling')], max_length=200, verbose_name='Relation')),
                ('contact_no', models.DecimalField(decimal_places=0, max_digits=20, verbose_name='Mobile No.')),
                ('base_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family', to='workforce.BasicProfile')),
            ],
            options={
                'verbose_name': 'Family & Dependents',
                'verbose_name_plural': 'Family & Dependents',
            },
        ),
    ]