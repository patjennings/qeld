# Generated by Django 4.2.3 on 2023-08-14 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season_manager', '0023_remove_game_game_coordinates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ground',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='game_ground',
            field=models.IntegerField(default=0),
        ),
    ]
