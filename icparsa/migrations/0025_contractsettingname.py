# Generated by Django 5.0.2 on 2024-05-14 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icparsa', '0024_contracthistory_renewalcounter'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractSettingName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]
