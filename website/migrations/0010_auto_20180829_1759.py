# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-08-29 17:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expansion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expansion_bgg_id', models.IntegerField()),
                ('expansion_name', models.CharField(max_length=500)),
                ('expansion_image', models.ImageField(upload_to='')),
                ('boardgame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_bg', to='website.Boardgame')),
            ],
        ),
        migrations.RemoveField(
            model_name='boardgameexpansion',
            name='boardgame',
        ),
        migrations.RemoveField(
            model_name='boardgameexpansion',
            name='boardgame_expansion',
        ),
        migrations.DeleteModel(
            name='BoardgameExpansion',
        ),
    ]