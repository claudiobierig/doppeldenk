# Generated by Django 2.1.5 on 2019-05-30 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacetrading', '0014_game_resource_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='midgame_scoring',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='midgame_scoring_event_move',
            field=models.IntegerField(default=-10),
        ),
        migrations.AddField(
            model_name='game',
            name='midgame_scoring_event_time',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='planet',
            name='planet_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
