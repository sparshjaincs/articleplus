# Generated by Django 2.2.6 on 2020-07-15 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20200715_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 15, 17, 27, 10, 779371)),
        ),
        migrations.AlterField(
            model_name='articles',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 15, 17, 27, 10, 771371)),
        ),
        migrations.DeleteModel(
            name='titleview',
        ),
    ]
