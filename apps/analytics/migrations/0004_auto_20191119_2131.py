# Generated by Django 2.1.7 on 2019-11-20 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0003_clienterror"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clienterror",
            name="error_body",
            field=models.TextField(max_length=2048),
        ),
    ]
