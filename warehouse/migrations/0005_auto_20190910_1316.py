# Generated by Django 2.1.1 on 2019-09-10 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_auto_20190910_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incoming',
            name='project_site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_project_site', to='workforce.ProjectSite'),
        ),
    ]
