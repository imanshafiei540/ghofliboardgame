# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-08-31 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_forum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_bgg_id', models.IntegerField()),
                ('credit_kind', models.CharField(max_length=200)),
                ('credit_title', models.CharField(max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='artisttoboardgame',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='artisttoboardgame',
            name='boardgame',
        ),
        migrations.RemoveField(
            model_name='designertoboardgame',
            name='boardgame',
        ),
        migrations.RemoveField(
            model_name='designertoboardgame',
            name='designer',
        ),
        migrations.AddField(
            model_name='boardgame',
            name='year_published',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Artist',
        ),
        migrations.DeleteModel(
            name='ArtistToBoardgame',
        ),
        migrations.DeleteModel(
            name='Designer',
        ),
        migrations.DeleteModel(
            name='DesignerToBoardgame',
        ),
        migrations.AddField(
            model_name='credit',
            name='boardgame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_bg', to='website.Boardgame'),
        ),
    ]