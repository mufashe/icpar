# Generated by Django 5.0.2 on 2024-04-02 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveMan', '0002_leave_delete_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='leave_days',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]