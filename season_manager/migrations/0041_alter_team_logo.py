# Generated by Django 4.2.3 on 2023-10-02 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0040_alter_game_game_team_away_alter_game_game_team_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='logo',
            field=models.CharField(max_length=255),
        ),
    ]
