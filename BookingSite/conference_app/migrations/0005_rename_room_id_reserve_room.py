# Generated by Django 3.2.9 on 2021-11-13 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference_app', '0004_reserve'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reserve',
            old_name='room_id',
            new_name='room',
        ),
    ]
