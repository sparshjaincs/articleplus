# Generated by Django 2.2.6 on 2020-07-19 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0026_auto_20200719_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 19, 18, 0, 45, 513571)),
        ),
    ]
