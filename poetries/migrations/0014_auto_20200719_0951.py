# Generated by Django 2.2.6 on 2020-07-19 04:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poetries', '0013_auto_20200715_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poetries',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 19, 9, 51, 33, 875267)),
        ),
    ]
