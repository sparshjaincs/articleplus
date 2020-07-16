# Generated by Django 2.2.6 on 2020-07-15 16:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0016_auto_20200715_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 15, 22, 3, 36, 372682)),
        ),
        migrations.AlterField(
            model_name='articles',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 7, 15, 22, 3, 36, 362655)),
        ),
        migrations.CreateModel(
            name='titleview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addr', models.CharField(blank=True, max_length=300, null=True)),
                ('view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titleview', to='article.Articles')),
            ],
        ),
    ]