# Generated by Django 4.2.11 on 2024-04-17 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("appOne", "0010_alter_equipment_admin_alter_equipment_reservation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staff",
            name="person_ptr",
        ),
        migrations.RemoveField(
            model_name="student",
            name="person_ptr",
        ),
        migrations.RemoveField(
            model_name="equipment",
            name="admin",
        ),
        migrations.AddField(
            model_name="reservation",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="Admin",
        ),
        migrations.DeleteModel(
            name="Staff",
        ),
        migrations.DeleteModel(
            name="Student",
        ),
    ]
