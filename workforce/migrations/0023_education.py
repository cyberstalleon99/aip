# Generated by Django 2.1.1 on 2018-12-20 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workforce', '0022_auto_20181220_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=500, verbose_name='Level of Attainment')),
                ('school', models.CharField(max_length=500, verbose_name='School')),
                ('start_year', models.DateField(verbose_name='Start Year')),
                ('end_year', models.DateField(verbose_name='End Year')),
                ('remarks', models.CharField(max_length=500, verbose_name='School')),
                ('base_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='workforce.BasicProfile')),
            ],
            options={
                'verbose_name': 'Educational Background',
                'verbose_name_plural': 'Educational Background',
            },
        ),
    ]