# Generated by Django 2.2.6 on 2020-07-19 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0023_auto_20200719_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 19, 18, 0, 45, 535629)),
        ),
        migrations.AlterField(
            model_name='articles',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 19, 18, 0, 45, 525602)),
        ),
    ]
