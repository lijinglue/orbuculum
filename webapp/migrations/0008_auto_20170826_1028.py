# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-26 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20170826_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='clear_timestamp',
            field=models.DateTimeField(blank=True),
        ),
    ]
