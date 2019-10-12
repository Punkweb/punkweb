# Generated by Django 2.1.7 on 2019-10-12 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20191012_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artistevent',
            name='address',
        ),
        migrations.AddField(
            model_name='artistevent',
            name='address_line',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='artistevent',
            name='city',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='artistevent',
            name='country',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='artistevent',
            name='state',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='artistevent',
            name='zip_code',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
