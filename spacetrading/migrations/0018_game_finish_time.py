# Generated by Django 2.2.3 on 2019-07-21 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacetrading', '0017_auto_20190612_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='finish_time',
            field=models.IntegerField(default=100),
        ),
    ]
