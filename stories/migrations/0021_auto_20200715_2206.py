# Generated by Django 2.2.6 on 2020-07-15 16:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0020_auto_20200715_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 15, 22, 6, 22, 157255)),
        ),
    ]
