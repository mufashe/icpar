# Generated by Django 5.0.2 on 2024-05-14 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icparsa', '0026_contractsetting_contractname'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='contractCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='icparsa.contractsettingname'),
        ),
    ]
