# Generated by Django 2.2.6 on 2020-07-14 03:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0011_auto_20200714_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 14, 9, 21, 6, 111625)),
        ),
    ]
