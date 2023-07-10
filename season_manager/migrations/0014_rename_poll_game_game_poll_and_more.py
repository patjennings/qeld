# Generated by Django 4.2.2 on 2023-07-10 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0013_rename_game_goals_assists_game_game_assists_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='poll',
            new_name='game_poll',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='type',
            new_name='game_type',
        ),
        migrations.AddField(
            model_name='game',
            name='game_redcards',
            field=models.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='game',
            name='game_yellowcards',
            field=models.JSONField(default=[]),
        ),
    ]
