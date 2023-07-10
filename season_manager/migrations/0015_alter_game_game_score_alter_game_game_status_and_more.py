# Generated by Django 4.2.2 on 2023-07-10 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0014_rename_poll_game_game_poll_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_score',
            field=models.CharField(default='0-0', max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_status',
            field=models.CharField(default='planned', max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='goals_against',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='goals_for',
            field=models.IntegerField(default=0),
        ),
    ]