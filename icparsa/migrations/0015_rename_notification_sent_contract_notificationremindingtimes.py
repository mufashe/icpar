# Generated by Django 5.0.2 on 2024-05-02 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icparsa', '0014_contractsetting_notificationsdaystowait'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='notification_Sent',
            new_name='notificationRemindingTimes',
        ),
    ]
