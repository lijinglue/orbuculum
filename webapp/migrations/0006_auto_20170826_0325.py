# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-26 03:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20170826_0235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='isMature',
            new_name='is_cleared',
        ),
    ]