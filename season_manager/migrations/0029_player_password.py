# Generated by Django 4.2.3 on 2023-08-17 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0028_alter_game_game_ground'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='password',
            field=models.CharField(default='', max_length=255),
        ),
    ]
