# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-27 13:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_prediction_close_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoitem',
            name='owner',
        ),
        migrations.AlterField(
            model_name='prediction',
            name='close_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Close at'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='start_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Open at'),
        ),
        migrations.DeleteModel(
            name='ToDoItem',
        ),
    ]
