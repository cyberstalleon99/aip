# Generated by Django 2.1.1 on 2020-02-18 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_auto_20200205_1553'),
        ('fleet', '0017_auto_20200211_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(verbose_name='Remarks')),
                ('base_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tools_attached', to='fleet.UnitProfile')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_tools', to='accounting.Item')),
            ],
            options={
                'verbose_name': 'Tool',
                'verbose_name_plural': 'Tools',
            },
        ),
    ]
