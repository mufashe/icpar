# Generated by Django 5.0.2 on 2024-08-06 09:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveMan', '0011_alter_leavedecision_approvingemployee'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavedecision',
            name='approvingEmployee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_leaves', to=settings.AUTH_USER_MODEL),
        ),
    ]
