# Generated by Django 2.1.7 on 2019-10-12 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20191012_1659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artistevent',
            options={'ordering': ('-event_date',)},
        ),
        migrations.RemoveField(
            model_name='artistevent',
            name='title',
        ),
    ]
