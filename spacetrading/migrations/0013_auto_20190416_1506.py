# Generated by Django 2.1.5 on 2019-04-16 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacetrading', '0012_auto_20190416_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]