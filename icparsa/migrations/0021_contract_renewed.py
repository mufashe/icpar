# Generated by Django 5.0.2 on 2024-05-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icparsa', '0020_alter_contractsetting_renewtimes'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='renewed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
