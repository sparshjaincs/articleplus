# Generated by Django 2.2.6 on 2020-07-13 05:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20200711_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 13, 11, 11, 38, 930132)),
        ),
        migrations.AlterField(
            model_name='articles',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 13, 11, 11, 38, 922128)),
        ),
    ]