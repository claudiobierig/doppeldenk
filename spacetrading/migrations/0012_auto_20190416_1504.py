# Generated by Django 2.1.5 on 2019-04-16 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacetrading', '0011_auto_20190319_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
