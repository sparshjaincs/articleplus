# Generated by Django 2.2.6 on 2020-07-25 05:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0027_auto_20200719_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 25, 11, 15, 4, 970879)),
        ),
    ]
