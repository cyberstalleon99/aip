# Generated by Django 2.1.15 on 2021-04-13 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0079_auto_20210408_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('head', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='workforce.BasicProfile')),
            ],
        ),
    ]