# Generated by Django 2.1.7 on 2019-10-21 09:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AnalyticsEvent",
            fields=[
                ("occurred_at", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("category", models.CharField(max_length=256)),
                ("action", models.CharField(max_length=256)),
                ("label", models.CharField(max_length=256)),
                (
                    "metadata",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
            ],
            options={
                "ordering": ("category", "action", "label"),
            },
        ),
    ]
