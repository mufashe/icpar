# Generated by Django 5.0.2 on 2024-05-03 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icparsa', '0017_contractsetting_managingemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
