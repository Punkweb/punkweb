# Generated by Django 4.2.11 on 2024-04-09 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0004_auto_20191119_2131"),
    ]

    operations = [
        migrations.AlterField(
            model_name="analyticsevent",
            name="metadata",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
