# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-08-29 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_file_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(max_length=500)),
                ('bgg_video_id', models.IntegerField()),
                ('video_category', models.CharField(max_length=250)),
                ('youtube_video_id', models.CharField(max_length=50)),
                ('video_post_date', models.CharField(max_length=250)),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Boardgame')),
            ],
        ),
    ]
