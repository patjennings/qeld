# Generated by Django 4.2.2 on 2023-07-10 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0015_alter_game_game_score_alter_game_game_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='absent',
            field=models.JSONField(default=[]),
        ),
        migrations.AlterField(
            model_name='poll',
            name='audience',
            field=models.JSONField(default=[]),
        ),
        migrations.AlterField(
            model_name='poll',
            name='present',
            field=models.JSONField(default=[]),
        ),
    ]