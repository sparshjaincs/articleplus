# Generated by Django 2.2.6 on 2020-07-13 12:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0005_auto_20200713_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 13, 17, 36, 43, 659190)),
        ),
        migrations.CreateModel(
            name='titleview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addr', models.CharField(blank=True, max_length=300, null=True)),
                ('view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titleview', to='stories.Stories', to_field='title')),
            ],
        ),
    ]
