# Generated by Django 5.0.2 on 2024-03-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icparsa', '0003_contract_departmentunit'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentmember',
            name='email',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
