# Generated by Django 2.2.6 on 2020-07-15 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poetries', '0010_auto_20200715_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poetries',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 15, 21, 48, 37, 710655)),
        ),
    ]