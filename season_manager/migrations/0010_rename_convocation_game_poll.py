# Generated by Django 4.2.2 on 2023-07-09 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0009_rename_convocation_poll'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='convocation',
            new_name='poll',
        ),
    ]
