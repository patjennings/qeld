# Generated by Django 4.2.3 on 2023-08-16 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0026_remove_game_game_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_poll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='season_manager.poll'),
        ),
    ]
