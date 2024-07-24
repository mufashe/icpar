# Generated by Django 5.0.2 on 2024-03-27 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('hire_date', models.DateField(blank=True, null=True)),
                ('home_phone', models.IntegerField(blank=True, null=True)),
                ('mobile_phone', models.IntegerField(blank=True, null=True)),
                ('home_address', models.CharField(blank=True, max_length=150, null=True)),
                ('months_in_institution', models.IntegerField(blank=True, null=True)),
                ('total_leave_days', models.IntegerField(blank=True, null=True)),
                ('leave_days_used', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
