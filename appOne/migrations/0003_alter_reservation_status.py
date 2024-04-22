# Generated by Django 4.2.11 on 2024-04-21 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appOne", "0002_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("approved", "Approved"), ("rejected", "Rejected")],
                max_length=255,
                null=True,
            ),
        ),
    ]