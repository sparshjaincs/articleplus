# Generated by Django 2.2.6 on 2020-07-15 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_auto_20200714_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotes',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 15, 17, 19, 37, 881411)),
        ),
    ]
