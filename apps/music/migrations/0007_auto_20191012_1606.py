# Generated by Django 2.1.7 on 2019-10-12 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_artistevent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ('artist', 'title', '-release_date')},
        ),
        migrations.RenameField(
            model_name='album',
            old_name='year',
            new_name='release_date',
        ),
    ]
