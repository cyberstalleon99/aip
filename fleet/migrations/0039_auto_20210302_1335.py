# Generated by Django 2.1.1 on 2021-03-02 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0076_subcon_status'),
        ('fleet', '0038_travel_arrived_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel',
            name='date_end',
        ),
        migrations.AddField(
            model_name='travel',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='travel_dest', to='workforce.ProjectSite'),
        ),
        migrations.AddField(
            model_name='travel',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='travel_source', to='workforce.ProjectSite'),
        ),
    ]
