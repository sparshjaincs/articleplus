# Generated by Django 2.2.6 on 2020-07-11 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 11, 21, 29, 37, 118824)),
        ),
        migrations.AlterField(
            model_name='articles',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 11, 21, 29, 37, 103221)),
        ),
    ]
