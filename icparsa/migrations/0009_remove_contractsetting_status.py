# Generated by Django 5.0.2 on 2024-03-21 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icparsa', '0008_contractsetting_name_contractsetting_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractsetting',
            name='status',
        ),
    ]
