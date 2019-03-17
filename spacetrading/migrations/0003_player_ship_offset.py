# Generated by Django 2.1.5 on 2019-02-16 19:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacetrading', '0002_player_colour'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='ship_offset',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=(0, 0), size=2),
            preserve_default=False,
        ),
    ]