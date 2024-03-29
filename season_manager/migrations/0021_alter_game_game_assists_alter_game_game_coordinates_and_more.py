# Generated by Django 4.2.2 on 2023-07-11 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0020_alter_game_game_assists_alter_game_game_coordinates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_assists',
            field=models.CharField(default='[]', max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_coordinates',
            field=models.CharField(default='[]', max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_goals',
            field=models.CharField(default='[]', max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_redcards',
            field=models.CharField(default='[]', max_length=255),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_yellowcards',
            field=models.CharField(default='[]', max_length=255),
        ),
        migrations.AlterField(
            model_name='poll',
            name='absent',
            field=models.CharField(default='[]', max_length=255),
        ),
        migrations.AlterField(
            model_name='poll',
            name='audience',
            field=models.CharField(default='[]', max_length=255),
        ),
        migrations.AlterField(
            model_name='poll',
            name='present',
            field=models.CharField(default='[]', max_length=255),
        ),
    ]
