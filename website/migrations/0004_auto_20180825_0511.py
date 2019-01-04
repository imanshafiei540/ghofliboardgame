# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-08-25 05:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_family_familytoboardgame'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorytoboardgame',
            name='type',
        ),
        migrations.RemoveField(
            model_name='familytoboardgame',
            name='type',
        ),
        migrations.RemoveField(
            model_name='mechanictoboardgame',
            name='type',
        ),
        migrations.AddField(
            model_name='categorytoboardgame',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='website.Category'),
        ),
        migrations.AddField(
            model_name='familytoboardgame',
            name='family',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='website.Family'),
        ),
        migrations.AddField(
            model_name='mechanictoboardgame',
            name='mechanic',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='website.Mechanic'),
        ),
    ]