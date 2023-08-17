# Generated by Django 4.2.3 on 2023-08-17 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0030_alter_game_game_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_status',
            field=models.CharField(choices=[('planned', 'Planned'), ('delayed', 'Delayed'), ('played', 'Played')], default='planned', max_length=255),
        ),
    ]
