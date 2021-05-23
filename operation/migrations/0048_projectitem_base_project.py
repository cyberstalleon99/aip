# Generated by Django 2.1.1 on 2019-06-13 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0047_projectitem_create_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectitem',
            name='base_project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='project_item', to='operation.Project'),
            preserve_default=False,
        ),
    ]
