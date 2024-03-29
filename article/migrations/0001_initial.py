# Generated by Django 2.2.6 on 2020-07-11 15:43

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=' ', max_length=150, unique=True)),
                ('project_name', models.CharField(max_length=100)),
                ('author', models.CharField(blank=True, max_length=50)),
                ('date_Publish', models.DateField(default=datetime.datetime.now)),
                ('date_updated', models.DateField(default=datetime.datetime.now)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='users/images')),
                ('video', models.FileField(blank=True, null=True, upload_to='users/video', verbose_name='Video')),
                ('image2', models.CharField(blank=True, max_length=1000, null=True)),
                ('content', ckeditor.fields.RichTextField(null=True)),
                ('link', models.TextField(blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
                ('time', models.TimeField(default=datetime.datetime(2020, 7, 11, 21, 12, 57, 611854))),
                ('tags', models.CharField(default='', help_text='Add comma( ,) seperated tags!!', max_length=300, null=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10)),
                ('method', models.CharField(choices=[('content', 'content'), ('design', 'design'), ('editor', 'editor')], default='content', max_length=10)),
                ('template', models.CharField(blank=True, max_length=1000, null=True)),
                ('quora', models.CharField(blank=True, max_length=1000, null=True)),
                ('medium', models.CharField(blank=True, max_length=1000, null=True)),
                ('facebook', models.CharField(blank=True, max_length=1000, null=True)),
                ('instagram', models.CharField(blank=True, max_length=1000, null=True)),
                ('twitter', models.CharField(blank=True, max_length=1000, null=True)),
                ('other', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'ordering': ('date_Publish', 'time'),
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(default='', max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='titleview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addr', models.CharField(blank=True, max_length=300, null=True)),
                ('view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titleview', to='article.Articles', to_field='title')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default='---', max_length=50)),
                ('last_name', models.CharField(blank=True, default='---', max_length=50)),
                ('email', models.EmailField(blank=True, default='---', max_length=50)),
                ('phone_number', models.CharField(blank=True, default='---', max_length=13)),
                ('avatar', models.ImageField(default='users/avatar/default.jpg', upload_to='users/avatar')),
                ('bio', models.TextField(blank=True, default='---')),
                ('address', models.CharField(blank=True, default='---', max_length=50)),
                ('city', models.CharField(blank=True, default='---', max_length=50)),
                ('state', models.CharField(blank=True, default='---', max_length=50)),
                ('country', models.CharField(blank=True, default='---', max_length=50)),
                ('date_of_birth', models.CharField(blank=True, default='---', max_length=13)),
                ('signup_confirmation', models.BooleanField(default=False)),
                ('medium', models.CharField(blank=True, max_length=1000, null=True)),
                ('quora', models.CharField(blank=True, max_length=1000, null=True)),
                ('other', models.CharField(blank=True, max_length=1000, null=True)),
                ('fav_stories', models.ManyToManyField(blank=True, related_name='stories_titles', to='stories.Stories')),
                ('favourities', models.ManyToManyField(blank=True, related_name='articles_titles', to='article.Articles')),
                ('follow', models.ManyToManyField(blank=True, default=None, related_name='follow_title', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, default=None, related_name='following_title', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_count', models.IntegerField(default=0)),
                ('activity_profile_count', models.IntegerField(default=0)),
                ('follow_count', models.IntegerField(default=0)),
                ('following_count', models.IntegerField(default=0)),
                ('user_name4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_name4_notification', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='my_comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.my_comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_comments', to='article.Articles')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='articles',
            name='category',
            field=models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, related_name='category', to='article.Categories', to_field='category_name'),
        ),
        migrations.AddField(
            model_name='articles',
            name='disliked',
            field=models.ManyToManyField(blank=True, default=None, related_name='dislikes_title', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articles',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='likes_title', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articles',
            name='user_name2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_username_2', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
        migrations.CreateModel(
            name='activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_activity', models.CharField(blank=True, max_length=200)),
                ('activity_icon', models.CharField(blank=True, max_length=200)),
                ('activity_time', models.TimeField(default=datetime.datetime(2020, 7, 11, 21, 12, 57, 624888))),
                ('date_activity', models.DateField(default=datetime.datetime.now)),
                ('activity_count', models.IntegerField(default=0, null=True)),
                ('user_name3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_username_3', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
    ]
