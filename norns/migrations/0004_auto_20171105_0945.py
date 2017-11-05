# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-05 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('norns', '0003_auto_20171105_0634'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='account',
            new_name='owner',
        ),
        migrations.AddField(
            model_name='dialogue',
            name='name',
            field=models.CharField(default='unnamed dialogue', max_length=64),
        ),
    ]