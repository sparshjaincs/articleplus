# Generated by Django 2.2.6 on 2020-07-14 03:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poetries', '0002_auto_20200714_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poetries',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 14, 9, 6, 47, 189868)),
        ),
    ]
