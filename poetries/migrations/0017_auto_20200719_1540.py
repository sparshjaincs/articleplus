# Generated by Django 2.2.6 on 2020-07-19 10:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poetries', '0016_auto_20200719_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poetries',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 19, 15, 40, 54, 906265)),
        ),
    ]
