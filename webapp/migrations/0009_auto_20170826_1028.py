# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-26 10:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20170826_1028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prediction',
            old_name='startAt',
            new_name='start_at',
        ),
    ]
